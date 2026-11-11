# Phase 01

- Creates two containers with one shared volume. 
- One container is running the updater script to fetch the dad jokes from the api and create the html page. It fetches a new joke every 30 seconds. The html is written into the shared html volume.
- The second container is running nginx and this is serving the html page that is in the shared volume.
- The updater container is running as the ubuntu user that ships with the container. It does not have root access.

```bash
# To build and run the container
docker compose up -d --build

# Inspect the logs
docker compose logs -f
```

The page is served on http://localhost:8080

## Notes
Had to modify the docker compose file to ensure the updater image started first. Otherwise, if nginx starts up before updater it copies files into the shared volume and sets permissions that prevents the updater from writing files. This wasn't an issue when running the container as root. The `nocopy true` stops nginx from copying in its default files. The updater now owns the volume and write its files,
