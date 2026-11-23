# Phase 2 - Public with TLS

## What it contains

- **backend**: FastAPI on port 8080 (`/`, `\health`, `/joke`. Runs as a non root user. Caches a joke for 25s and will fall back to the last good joke if the upstream API is down.
- **web**: nginx-unprivileged serving a static page that calls the FastAPI every 30s.
- **cloudflaretunnel**: remotely managed tunnel. No inbound ports are open.

## Build Notes

- The docker compose file will build the frontend and backend containers and also spin up the nginx and cloudflared containers.

```bash
docker compose up -d --build
```

- To build and scan the containers for vulnerabilities run the following command

```bash
./build-scan.sh
```

## Config

| Variable | Where | Default | Description |
| --- | --- | --- | --- |
| `TUNNEL_TOKEN` | `.env` (never comitted) | none | cloudflared auth |
| `CACHE_SECONDS` | backend | 25 | joke cache TTL |
| `TUNNEL_METRICS` | cloudflaretunnel | 127.0.0.1:20241 | metrics + healthcheck |
