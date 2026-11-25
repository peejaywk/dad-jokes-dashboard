import time
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException

from .config import (
    API_HOST,
    API_PORT,
    APP_NAME,
    CACHE_SECONDS,
)

JOKE_URL = "https://icanhazdadjoke.com/"

cache = {"joke": None, "fetched_at": 0.0}

# This is a comment to trigger the CI pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create one HTTP client when the app starts and reuse it for every request.
    # This is faster than opening a new connection each time.
    app.state.client = httpx.AsyncClient(
        timeout=5.0,  # don't let a slow joke API hang our API
        headers={
            "Accept": "application/json",  # ask for JSON instead of HTML
            "User-Agent": "dad-jokes-dashboard (https://github.com/peejaywk/dad-jokes-dashboard)",
        },
    )
    yield
    # Close the client cleanly when the app shuts down.
    await app.state.client.aclose()


app = FastAPI(title=APP_NAME, lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Dad Jokes Dashboard API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/joke")
async def joke():
    age = time.monotonic() - cache["fetched_at"]

    # Joke is still fresh so answer from memory, no upstream call required.
    if cache["joke"] and age < CACHE_SECONDS:
        return {"joke": cache["joke"], "source": "cache", "age_seconds": int(age)}

    # Joke is too old, or empty, so fetch a new one.
    try:
        response = await app.state.client.get(JOKE_URL)
        response.raise_for_status()  # treat 4xx/5xx as an error
        cache["joke"] = response.json()["joke"]
        cache["fetched_at"] = time.monotonic()
        return {"joke": cache["joke"], "source": "live"}

    # Upstream failed. Serve the old joke if we have one, else 503
    except (httpx.HTTPError, ValueError, KeyError):
        if cache["joke"]:
            return {"joke": cache["joke"], "source": "stale"}
        raise HTTPException(
            status_code=503, detail="Joke API unavailable, nothing cached yet"
        )


def main():
    """Entry point for running the API server"""
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=False)


if __name__ == "__main__":
    main()
