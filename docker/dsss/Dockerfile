FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy ONLY backend code + pyproject
COPY ../../pyproject.toml ../../README.md /app/
COPY ../../dsss /app/dsss

RUN pdm install --prod --without dev

EXPOSE 8000
CMD ["pdm", "run", "python", "-m", "dsss.main"]

