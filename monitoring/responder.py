import subprocess


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
    else:
        print("Failed to restart application")
        print(result.stderr)
        return False


if __name__ == "__main__":
    restart_application()