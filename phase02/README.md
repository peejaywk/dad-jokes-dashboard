# Phase 2

## Objectives

- Replace the bash updater script with a Python fetcher API using FastAPI.
- Create a Cloudflare tunnel with a public host name so the dad jokes dashboard can be accessed securely from the internet without opening any inbound ports.
- Add the Cloudflare service to the docker compose build file.
- Ensure the Cloudflare tunnel token is only stored locally and not commit to this repository.
- Create a new frontend deployment to access the Python FastAPI to retrieve and display the jokes.

## Build Notes

- The docker compose file will build the frontend and backend containers and also spin up the nginx and cloudflared containers.

```
docker compose up -d
```

- To build and scan the containers for vulnerabilities run the following command

```
./build-scan.sh
```
