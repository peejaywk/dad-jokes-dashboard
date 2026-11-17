from contextlib import asynccontextmanager
import uvicorn
import httpx
from fastapi import FastAPI

from .config import (
    APP_NAME,
    API_HOST,
    API_PORT,
)

JOKE_URL = "https://icanhazdadjoke.com/"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create one HTTP client when the app starts and reuse it for every request.
    # This is faster than opening a new connection each time.
    app.state.client = httpx.AsyncClient(
        timeout=5.0,  # don't let a slow joke API hang our API
        headers={
            "Accept": "application/json",  # ask for JSON instead of HTML
            "User-Agent": "my-joke-api (https://github.com/yourname/repo)",
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
    response = await app.state.client.get(JOKE_URL)

    data = response.json()
    return data


def main():
    """Entry point for running the API server"""
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=True)


if __name__ == "__main__":
    main()
