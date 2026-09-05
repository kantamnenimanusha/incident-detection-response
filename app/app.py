"""
app.py

Incident Response App
----------------------
A small Flask application that acts as the "target application" for a
DevOps Incident Detection & Response project. A future monitoring script
will call /health and /status on this app to check if it is alive and well.

This app also includes a CONTROLLED (non-random) way to simulate failures,
so you can test your monitoring/incident-response system on demand.
"""

import time
import logging

from flask import Flask, jsonify, request

from config import Config

# ---------------------------------------------------------------------------
# Logging setup
# Logs are written to stdout with timestamps and levels, so Docker (and any
# log-collection tool you add later) can capture and read them easily.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("incident-response-app")

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Application state
# ---------------------------------------------------------------------------
SERVICE_NAME = "incident-response-app"
START_TIME = time.time()

# The only failure modes this app understands. Anything else is rejected.
VALID_FAILURE_MODES = {"none", "unhealthy", "slow", "error"}

# current_failure_mode is a simple in-memory switch.
# It NEVER changes on its own — it only changes when:
#   1) the app starts, using the FAILURE_MODE environment variable, or
#   2) you call POST /test/simulate-failure (only when TESTING_MODE=true)
# This makes failure simulation fully controlled and repeatable, not random.
if Config.DEFAULT_FAILURE_MODE in VALID_FAILURE_MODES:
    current_failure_mode = Config.DEFAULT_FAILURE_MODE
else:
    current_failure_mode = "none"

logger.info(
    "Starting %s | testing_mode=%s | initial_failure_mode=%s | port=%s",
    SERVICE_NAME, Config.TESTING_MODE, current_failure_mode, Config.PORT,
)


def get_uptime_seconds():
    return round(time.time() - START_TIME, 2)


# ---------------------------------------------------------------------------
# NORMAL APPLICATION ENDPOINTS
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    logger.info("GET / called")
    return "Incident Detection & Response application is running.", 200


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.

    This is the endpoint your future monitoring script should poll
    regularly (e.g. every few seconds) to detect incidents.

    Its behavior depends on `current_failure_mode`:
      - "none"      -> normal, healthy response (200)
      - "unhealthy" -> reports unhealthy status (503)
      - "error"     -> simulates a server error (500)
      - "slow"      -> deliberately delays the response (still 200),
                       useful for testing latency/timeout detection
    """
    global current_failure_mode

    if current_failure_mode == "slow":
        logger.warning("Simulating SLOW response on /health (5 second delay)")
        time.sleep(5)

    if current_failure_mode == "error":
        logger.error("Simulating ERROR response on /health")
        return jsonify({
            "status": "error",
            "service": SERVICE_NAME,
            "message": "Simulated internal error for testing purposes"
        }), 500

    if current_failure_mode == "unhealthy":
        logger.warning("Simulating UNHEALTHY status on /health")
        return jsonify({
            "status": "unhealthy",
            "service": SERVICE_NAME
        }), 503

    logger.info("GET /health called - status healthy")
    return jsonify({
        "status": "healthy",
        "service": SERVICE_NAME
    }), 200


@app.route("/status", methods=["GET"])
def status():
    """
    Returns general application information: name, status, and uptime.
    Useful for dashboards or a monitoring script that wants more detail
    than a plain health check.
    """
    logger.info("GET /status called")
    return jsonify({
        "service": SERVICE_NAME,
        "status": "running",
        "uptime_seconds": get_uptime_seconds(),
        "current_failure_mode": current_failure_mode,
        "testing_mode_enabled": Config.TESTING_MODE,
    }), 200


# ---------------------------------------------------------------------------
# TESTING / FAILURE-SIMULATION ENDPOINTS
#
# These are clearly separated from the normal app functionality above.
# They only work when the TESTING_MODE environment variable is set to
# "true". This prevents them from being accidentally usable in a
# "production-like" run of the app.
# ---------------------------------------------------------------------------

@app.route("/test/simulate-failure", methods=["POST"])
def simulate_failure():
    """
    Intentionally turn on a failure mode.

    Example request body (JSON):
        { "mode": "unhealthy" }
        { "mode": "slow" }
        { "mode": "error" }
        { "mode": "none" }
    """
    global current_failure_mode

    if not Config.TESTING_MODE:
        logger.warning("Blocked call to /test/simulate-failure - TESTING_MODE is disabled")
        return jsonify({
            "error": "Testing mode is disabled. Set TESTING_MODE=true to use this endpoint."
        }), 403

    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "none")

    if mode not in VALID_FAILURE_MODES:
        return jsonify({
            "error": f"Invalid mode '{mode}'.",
            "valid_modes": sorted(VALID_FAILURE_MODES),
        }), 400

    current_failure_mode = mode
    logger.info("Failure mode manually changed to '%s'", current_failure_mode)
    return jsonify({
        "message": f"Failure mode set to '{current_failure_mode}'",
        "current_failure_mode": current_failure_mode,
    }), 200


@app.route("/test/reset", methods=["POST"])
def reset_failure():
    """Turn off any simulated failure and return to normal behavior."""
    global current_failure_mode

    if not Config.TESTING_MODE:
        logger.warning("Blocked call to /test/reset - TESTING_MODE is disabled")
        return jsonify({
            "error": "Testing mode is disabled. Set TESTING_MODE=true to use this endpoint."
        }), 403

    current_failure_mode = "none"
    logger.info("Failure mode reset to 'none'")
    return jsonify({
        "message": "Failure mode reset to 'none'",
        "current_failure_mode": current_failure_mode,
    }), 200


@app.route("/test/status", methods=["GET"])
def test_status():
    """Shows current testing configuration - useful while writing your monitoring script."""
    if not Config.TESTING_MODE:
        return jsonify({
            "error": "Testing mode is disabled. Set TESTING_MODE=true to use this endpoint."
        }), 403

    return jsonify({
        "testing_mode_enabled": Config.TESTING_MODE,
        "current_failure_mode": current_failure_mode,
        "valid_failure_modes": sorted(VALID_FAILURE_MODES),
    }), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=False)
