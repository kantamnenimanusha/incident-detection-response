import subprocess

from response_policy import get_response


def restart_application():
    print("Attempting to restart application...")

    result = subprocess.run(
        ["docker", "restart", "incident-response-container"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Application restarted successfully")
        return True

    print("Failed to restart application")
    print(result.stderr)
    return False


def respond_to_incident(incident):
    action = get_response(
        incident["type"],
        incident["severity"]
    )

    print("Response Policy:", action)

    if action == "RESTART_APPLICATION":
        return restart_application()

    if action == "MONITOR_AND_LOG":
        print("No automatic action required")
        print("Continuing to monitor the incident")
        return True

    print("No response action defined")
    return False


if __name__ == "__main__":

    incident = {
        "type": "Application",
        "severity": "CRITICAL"
    }

    respond_to_incident(incident)