import subprocess
import time
import csv
from datetime import datetime

from incident_manager import create_incident, resolve_incident

import os

CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80"))
MEMORY_THRESHOLD = float(os.getenv("MEMORY_THRESHOLD", "80"))

LOG_FILE = "logs/incidents.log"
HISTORY_FILE = "logs/incident_history.csv"


def get_cpu_usage():
    command = (
        "Get-Counter '\\Processor(_Total)\\% Processor Time' "
        "| Select-Object -ExpandProperty CounterSamples "
        "| Select-Object -ExpandProperty CookedValue"
    )

    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )

    return float(result.stdout.strip())


def get_memory_usage():
    command = (
        "Get-Counter '\\Memory\\% Committed Bytes In Use' "
        "| Select-Object -ExpandProperty CounterSamples "
        "| Select-Object -ExpandProperty CookedValue"
    )

    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )

    return float(result.stdout.strip())


def log_incident(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"{current_time} | {message}\n")

def get_active_incident(subtype):
    active_incident = None

    try:
        with open(HISTORY_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for incident in reader:
                if (
                    incident.get("Type") == "Resource"
                    and incident.get("Subtype", "") == subtype
                    and incident.get("Status") == "ACTIVE"
                ):
                    active_incident = incident

    except FileNotFoundError:
        return None

    return active_incident


def monitor_resources():
    print("System Resource Monitor")
    print("-" * 40)

    cpu_incident = get_active_incident("CPU")
    memory_incident = get_active_incident("MEMORY")

    cpu_incident_active = cpu_incident is not None
    memory_incident_active = memory_incident is not None

    if cpu_incident_active:
        print("Existing active CPU incident found")
        print("Incident ID:", cpu_incident["ID"])

    if memory_incident_active:
        print("Existing active memory incident found")
        print("Incident ID:", memory_incident["ID"])

    while True:
        cpu = get_cpu_usage()
        memory = get_memory_usage()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{current_time}] CPU Usage: {cpu:.2f}%")
        print(f"[{current_time}] Memory Usage: {memory:.2f}%")

        # CPU monitoring
        if cpu > CPU_THRESHOLD:
            print("INCIDENT: High CPU usage detected")

            if not cpu_incident_active:
                message = f"High CPU usage detected: {cpu:.2f}%"

                cpu_incident = create_incident(
                    "Resource",
                    "WARNING",
                    message,
                    "CPU"
                )

                log_incident(f"INCIDENT | {message}")

                print("NEW CPU INCIDENT LOGGED")
                print("Incident ID:", cpu_incident["id"])

                cpu_incident_active = True

        else:
            if cpu_incident_active:
                resolve_incident(cpu_incident)

                log_incident(
                    f"RECOVERED | CPU usage returned to normal: {cpu:.2f}%"
                )

                print("CPU RECOVERY - Incident resolved")

                cpu_incident_active = False
                cpu_incident = None

        # Memory monitoring
        if memory > MEMORY_THRESHOLD:
            print("INCIDENT: High memory usage detected")

            if not memory_incident_active:
                message = f"High memory usage detected: {memory:.2f}%"

                memory_incident = create_incident(
                    "Resource",
                    "WARNING",
                    message,
                    "MEMORY"
                )

                log_incident(f"INCIDENT | {message}")

                print("NEW MEMORY INCIDENT LOGGED")
                print("Incident ID:", memory_incident["id"])

                memory_incident_active = True

        else:
            if memory_incident_active:
                resolve_incident(memory_incident)

                log_incident(
                    f"RECOVERED | Memory usage returned to normal: {memory:.2f}%"
                )

                print("MEMORY RECOVERY - Incident resolved")

                memory_incident_active = False
                memory_incident = None

        print("-" * 40)

        time.sleep(5)


if __name__ == "__main__":
    monitor_resources()