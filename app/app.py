import logging
import os
import socket

from flask import Flask, jsonify, request
import redis, time

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


# Endpoint de test pour Redis (set/get simple)
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


# Endpoint compteur basé sur Redis
@app.route("/counter")
def counter():
    """
    Incrémente un compteur stocké dans Redis et renvoie sa valeur.
    Clé utilisée : "visits_counter"
    """
    try:
        logger.info("Incrément du compteur Redis")
        value = redis_client.incr("visits_counter")  # INCR dans Redis
        return jsonify(
            counter=int(value)
        ), 200
    except redis.RedisError as exc:  # type: ignore[attr-defined]
        logger.error("Erreur Redis pendant /counter: %s", exc)
        return jsonify(error="Redis unavailable"), 500


@app.route("/limited")
def limited():
    ip = request.remote_addr  # adresse de l'utilisateur
    key = f"rate_limit:{ip}"

    try:
        # Incrémente le compteur
        count = redis_client.incr(key)

        # Si c'est le premier appel, on met une expiration de 60 secondes
        if count == 1:
            redis_client.expire(key, 60)

        # Limite : 5 requêtes par minute
        if count > 5:
            return jsonify(error="Too Many Requests"), 429

        return jsonify(
            message="Request allowed",
            remaining_requests=5 - count
        ), 200

    except redis.RedisError:
        return jsonify(error="Redis unavailable"), 500


@app.route("/slow")
def slow():
    """
    Simule un traitement long (2 secondes).
    """
    time.sleep(2)
    return jsonify(message="Slow response done"), 200


@app.route("/slow/cached")
def slow_cached():
    cache_key = "slow_result"

    try:
        # Vérifier si le résultat est en cache
        cached = redis_client.get(cache_key)
        if cached:
            return jsonify(
                cached=True,
                result=cached
            ), 200

        # Sinon exécuter la version lente
        time.sleep(2)
        result = "Slow response done"

        # Stocker dans Redis avec une expiration
        redis_client.set(cache_key, result)
        redis_client.expire(cache_key, 10)  # expire après 10s

        return jsonify(
            cached=False,
            result=result
        ), 200

    except redis.RedisError:
        return jsonify(error="Redis unavailable"), 500


# Mode développement (non utilisé en production où Gunicorn prend le relais)
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info("Lancement de l'application Flask en mode debug=%s", debug)
    app.run(host="0.0.0.0", port=5000, debug=debug)  # nosec B104
