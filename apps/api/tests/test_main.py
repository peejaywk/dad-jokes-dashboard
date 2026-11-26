from importlib.metadata import version as pkg_version

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import main

JOKE = "I'm reading a book on anti-gravity. I can't put it down."


def upstream_ok(request):
    return httpx.Response(200, json={"joke": JOKE})


def upstream_down(request):
    return httpx.Response(500)


def use_upstream(handler):
    main.app.state.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setitem(main.cache, "joke", None)
    monkeypatch.setitem(main.cache, "fetched_at", 0.0)
    with TestClient(main.app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}


def test_joke_live_then_cache(client):
    use_upstream(upstream_ok)
    first = client.get("/joke").json()
    second = client.get("/joke").json()
    assert first == {"joke": JOKE, "source": "live"}
    assert second["source"] == "cache"


def test_version(client):
    r = client.get("/version")
    assert r.status_code == 200
    assert r.json() == {"version": pkg_version("dad-jokes-dashboard-backend")}
