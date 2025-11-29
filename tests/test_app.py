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


def test_counter_increments(monkeypatch):
    class MockRedis:
        def __init__(self):
            self.value = 0

        def incr(self, key):
            # on ignore la clé, on incrémente juste une valeur
            self.value += 1
            return self.value

    mock = MockRedis()
    monkeypatch.setattr("app.app.redis_client", mock)

    client = app.test_client()

    # premier appel -> 1
    response1 = client.get("/counter")
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1["counter"] == 1

    # deuxième appel -> 2
    response2 = client.get("/counter")
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2["counter"] == 2


def test_limited_requests(monkeypatch):
    class MockRedis:
        def __init__(self):
            self.counter = 0

        def incr(self, key):
            self.counter += 1
            return self.counter

        def expire(self, key, seconds):
            pass

    mock = MockRedis()
    monkeypatch.setattr("app.app.redis_client", mock)

    client = app.test_client()

    # 5 premières requêtes -> OK
    for _ in range(5):
        r = client.get("/limited")
        assert r.status_code == 200

    # 6ème -> trop de requêtes
    r6 = client.get("/limited")
    assert r6.status_code == 429


def test_slow_cached(monkeypatch):
    class MockRedis:
        def __init__(self):
            self.store = {}

        def get(self, key):
            return self.store.get(key, None)

        def set(self, key, value):
            self.store[key] = value

        def expire(self, key, seconds):
            pass

    mock = MockRedis()
    monkeypatch.setattr("app.app.redis_client", mock)

    client = app.test_client()

    # Premier appel -> pas en cache
    r1 = client.get("/slow/cached")
    assert r1.status_code == 200
    assert r1.get_json()["cached"] is False

    # Deuxième appel -> en cache
    r2 = client.get("/slow/cached")
    assert r2.status_code == 200
    assert r2.get_json()["cached"] is True
