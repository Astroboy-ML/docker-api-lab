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
    # Le message doit commencer par notre texte
    assert data["message"].startswith("Hello from Dockerized API")
    # On vérifie que le hostname est bien présent et est une chaîne
    assert "hostname" in data
    assert isinstance(data["hostname"], str)
