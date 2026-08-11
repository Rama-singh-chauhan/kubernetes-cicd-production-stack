import os
import time

from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "appdb")
DB_USER = os.getenv("POSTGRES_USER", "appuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


@app.route("/")
def home():
    return jsonify({
        "application": "DevOps Infrastructure Challenge",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({
            "status": "not ready",
            "error": str(e)
        }), 503


@app.route("/db")
def database_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "database": "PostgreSQL",
            "status": "connected",
            "version": version
        })

    except Exception as e:
        return jsonify({
            "database": "PostgreSQL",
            "status": "connection failed",
            "error": str(e)
        }), 500


@app.route("/slow")
def slow():
    time.sleep(10)
    return jsonify({"message": "slow response"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
