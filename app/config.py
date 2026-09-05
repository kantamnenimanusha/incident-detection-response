"""
config.py

Centralized configuration for the Incident Response App.
All values are read from environment variables so behavior can be changed
without touching the code (important once this app runs inside Docker).
"""

import os


class Config:
    # Network settings
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    # Testing / failure-simulation settings
    # TESTING_MODE must be explicitly set to "true" to unlock the /test/* endpoints.
    TESTING_MODE = os.environ.get("TESTING_MODE", "false").lower() == "true"

    # Optional: set an initial failure mode at startup (useful for container tests).
    # Valid values: none, unhealthy, slow, error
    DEFAULT_FAILURE_MODE = os.environ.get("FAILURE_MODE", "none")

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
