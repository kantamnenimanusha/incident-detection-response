import urllib.request
import urllib.error
import time
from datetime import datetime

from responder import respond_to_incident
from incident_manager import create_incident, resolve_incident
from alert_manager import send_alert


HEALTH_URL = "http://127.0.0.1:5000/health"
CHECK_INTERVAL = 5
LOG_FILE = "logs/incidents.log"


def check_health():
    try:
        response = urllib.request.urlopen(HEALTH_URL, timeout=3)

        if response.status == 200:
            return True, "Application is healthy"

        return False, f"Application returned HTTP {response.status}"

    except urllib.error.HTTPError as error:
        return False, f"Application returned HTTP {error.code}"

    except Exception as error:
        return False, f"Application is unreachable: {error}"


def log_incident(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"{current_time} | {message}\n")


def monitor():
    print("Incident Monitoring System Started")
    print(f"Monitoring: {HEALTH_URL}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("-" * 50)

    incident_active = False
    current_incident = None

    while True:
        healthy, message = check_health()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if healthy:
            print(f"[{current_time}] HEALTHY - {message}")

            if incident_active:
                resolve_incident(current_incident)

                log_incident(
                    "RECOVERED | Application is healthy"
                )

                print(f"[{current_time}] RECOVERY - Incident resolved")

                incident_active = False
                current_incident = None

        else:
            print(f"[{current_time}] INCIDENT - {message}")

            if not incident_active:

                current_incident = create_incident(
                    "Application",
                    "CRITICAL",
                    message,
                    "HTTP"
                )

                log_incident(
                    f"INCIDENT | {message}"
                )

                print(f"[{current_time}] NEW INCIDENT LOGGED")
                print("Incident ID:", current_incident["id"])
                send_alert(current_incident)

                respond_to_incident(current_incident)

                incident_active = True

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()