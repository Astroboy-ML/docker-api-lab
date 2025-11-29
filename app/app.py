# bandit:ignore=B104

from flask import Flask, jsonify
import socket
import os

# Création de l'application Flask
app = Flask(__name__)


# Endpoint de santé utilisé pour les healthchecks Docker/Kubernetes
@app.route("/health")
def health():
    return jsonify(status="ok"), 200


# Endpoint d'information retournant un message + le hostname du container
@app.route("/info")
def info():
    return jsonify(
        message="Hello from Dockerized API 👋",
        hostname=socket.gethostname(),
    )


# Mode développement (non utilisé en production où Gunicorn prend le relais)
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
