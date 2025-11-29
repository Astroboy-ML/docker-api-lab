from app.app import app


def test_health_ok():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_info_ok():
    client = app.test_client()
    response = client.get("/info")

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"].startswith("Hello from Dockerized API")
    assert "hostname" in data
    assert isinstance(data["hostname"], str)


def test_cache_test_ok(monkeypatch):
    class MockRedis:
        def set(self, key, value):
            pass

        def get(self, key):
            return "Hello Redis!"

    # On remplace le vrai client Redis par un mock pour les tests
    monkeypatch.setattr("app.app.redis_client", MockRedis())

    client = app.test_client()
    response = client.get("/cache-test")

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Cache OK"
    assert data["cached_value"] == "Hello Redis!"
    