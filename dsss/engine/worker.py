import asyncio
from contextlib import suppress
import socket
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from dsss.checks.base import AsyncCheck, SyncCheck
from dsss.config import Config
from dsss.logger import get_logger

logger = get_logger("Workers")

MAGIC_READY_STR = b"bb123#123\n"


class CheckRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    team: str
    service: str


class CheckResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    success: bool
    message: str | None


class Worker:
    _current_worker_id: ClassVar[int] = 0

    process: asyncio.subprocess.Process | None
    reader: asyncio.StreamReader | None
    writer: asyncio.StreamWriter | None
    worker_id: int

    def __init__(self) -> None:
        self.process = None
        self.reader = None
        self.writer = None
        self.worker_id = Worker._current_worker_id

        Worker._current_worker_id += 1

    async def start(self) -> None:
        parent, child = socket.socketpair()

        try:
            async with asyncio.timeout(30):
                self.process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    "-m",
                    "dsss.main",
                    "check",
                    "--fd",
                    str(child.fileno()),
                    pass_fds=(child.fileno(),),
                    stdin=asyncio.subprocess.DEVNULL,
                )

                child.close()
                self.reader, self.writer = await asyncio.open_connection(sock=parent)

                if await self.reader.readline() != MAGIC_READY_STR:
                    raise RuntimeError("Check worker failed to start")

        except BaseException:
            await self.close()
            raise

        finally:
            child.close()
            if self.writer is None:
                parent.close()

    async def check(self, team: str, service: str) -> tuple[bool, str | None]:
        assert self.reader is not None and self.writer is not None

        request = CheckRequest(team=team, service=service)
        self.writer.write((request.model_dump_json() + "\n").encode())

        await self.writer.drain()
        line = await self.reader.readline()

        if not line:
            raise RuntimeError("Check worker exited without a result")

        result = CheckResponse.model_validate_json(line)
        return result.success, result.message

    async def close(self) -> None:
        process = self.process
        writer = self.writer

        try:
            if process is not None and process.returncode is None:
                with suppress(ProcessLookupError):
                    process.kill()

            if writer is not None:
                writer.close()

            if process is not None:
                try:
                    async with asyncio.timeout(2):
                        _ = await process.wait()

                except TimeoutError:
                    logger.warning(
                        "Worker with PID: %s did not exit after being killed",
                        process.pid,
                    )

            if writer is not None:
                try:
                    async with asyncio.timeout(1):
                        await writer.wait_closed()

                except (TimeoutError, ConnectionError):
                    pass
        finally:
            self.process = None
            self.reader = None
            self.writer = None


class WorkerPool:
    def __init__(self, size: int) -> None:
        self.workers: list[Worker] = [Worker() for _ in range(size)]
        self.idle: asyncio.Queue[Worker] = asyncio.Queue()

    async def __aenter__(self):
        # attempt to spawn all workers
        try:
            logger.debug("Spawning %s worker processes", len(self.workers))

            # we use return_exceptions here to ensure that all workers finish starting
            # before we handle any errors.
            # this prevent races where we might try to handle
            # cleanup with worker threads still spawning.
            results = await asyncio.gather(
                *(worker.start() for worker in self.workers), return_exceptions=True
            )

            for result in results:
                if isinstance(result, BaseException):
                    raise result

            for worker in self.workers:
                self.idle.put_nowait(worker)

            return self

        except BaseException:
            await self.__aexit__(None, None, None)
            raise

    async def __aexit__(self, _exc_type: None, exc_val: None, exc_tb: None):
        _ = await asyncio.gather(*(worker.close() for worker in self.workers))

    async def check(
        self, team: str, service: str, timeout: float
    ) -> tuple[bool, str | None]:
        """
        Attempts to reserve a worker from the idle queue and perform a check
        """
        worker = await self.idle.get()

        try:
            if worker.process is None:
                logger.warning(
                    "Worker process with ID: %s was not started at time of check, attempting to restart.",
                    worker.worker_id,
                )
                await worker.start()
            async with asyncio.timeout(timeout):
                return await worker.check(team, service)

        except asyncio.CancelledError:
            await worker.close()
            raise

        finally:
            self.idle.put_nowait(worker)


async def run_worker(config: Config, fd: int) -> None:
    reader, writer = await asyncio.open_connection(sock=socket.socket(fileno=fd))

    try:
        writer.write(MAGIC_READY_STR)
        await writer.drain()

        while line := await reader.readline():
            try:
                request = CheckRequest.model_validate_json(line)
                check = config.teams[request.team].services[request.service].check

                if isinstance(check, SyncCheck):
                    success, message = check.check()
                elif isinstance(check, AsyncCheck):
                    success, message = await check.check()
                else:
                    raise TypeError(f"Unsupported check type: {type(check).__name__}")

            except Exception as error:
                success, message = False, f"Error: {error}"

            # messages cannot exceed the stream limit of 64kb
            if message is not None:
                message = str(message)[:8192]

            response = CheckResponse(success=success, message=message)
            writer.write((response.model_dump_json() + "\n").encode())
            await writer.drain()
    finally:
        writer.close()
