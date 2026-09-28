import argparse
import asyncio
from pathlib import Path

from dsss.config.loader import ConfigError, load_config


def main():
    parser = argparse.ArgumentParser(description="Damiens' Simple Scoring Suite")
    parser.add_argument(
        "mode", choices=("server", "check", "validate"), nargs="?", default="server"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="TOML configuration (default: config.toml)",
    )
    parser.add_argument(
        "--fd", type=int, help="Private IPC socket supplied by the server"
    )
    args = parser.parse_args()
    if args.mode == "check" and args.fd is None:
        parser.error("check mode requires --fd")
    if args.mode != "check" and args.fd is not None:
        parser.error("--fd is only used in check mode")
    try:
        config = load_config(args.config)
    except ConfigError as error:
        parser.error(str(error))

    if args.mode == "validate":
        print(f"Valid configuration: {config.source_path} ({len(config.teams)} teams)")
    elif args.mode == "check":
        from dsss.engine.worker import run_worker

        asyncio.run(run_worker(config, args.fd))
    else:
        import uvicorn
        from dsss.api.api import app

        app.state.config = config
        uvicorn.run(app, host=config.host, port=config.port, log_level="error")


if __name__ == "__main__":
    main()
