import logging
import os
import socket

from flask import Flask, jsonify
import redis

# Configuration basique du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Création de l'application Flask
app = Flask(__name__)

# Client Redis (utilisé si REDIS est disponible, ex: via docker-compose)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


# Endpoint de santé utilisé pour les healthchecks Docker/Kubernetes
@app.route("/health")
def health():
    logger.info("Healthcheck appelé")
    return jsonify(status="ok"), 200


# Endpoint d'information retournant un message + le hostname du container
@app.route("/info")
def info():
    hostname = socket.gethostname()
    logger.info("Endpoint /info appelé depuis hostname=%s", hostname)
    return jsonify(
        message="Hello from Dockerized API 👋",
        hostname=hostname,
    ), 200


# Endpoint de test pour Redis
@app.route("/cache-test")
def cache_test():
    try:
        logger.info("Test du cache Redis")
        redis_client.set("test_key", "Hello Redis!")
        value = redis_client.get("test_key")
        return jsonify(
            message="Cache OK",
            cached_value=value,
        ), 200
    except redis.RedisError as exc:  # type: ignore[attr-defined]
        logger.error("Erreur Redis: %s", exc)
        return jsonify(error="Redis unavailable"), 500


# Mode développement (non utilisé en production où Gunicorn prend le relais)
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info("Lancement de l'application Flask en mode debug=%s", debug)
    app.run(host="0.0.0.0", port=5000, debug=debug)  # nosec B104
    
