import subprocess
import time
from datetime import datetime
from incident_manager import create_incident, resolve_incident


CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
LOG_FILE = "logs/incidents.log"


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


def monitor_resources():
    print("System Resource Monitor")
    print("-" * 40)

    cpu_incident_active = False
    memory_incident_active = False

    cpu_incident = None
    memory_incident = None

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
                    message
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
                    message
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