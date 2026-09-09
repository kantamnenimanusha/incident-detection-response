from datetime import datetime
import csv

incident_history = []
incident_counter = 0

HISTORY_FILE = "logs/incident_history.csv"


def create_incident(incident_type, severity, description, subtype=""):
    global incident_counter
    incident_counter += 1

    incident = {
        "id": "INC-" + datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(incident_counter),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": incident_type,
        "subtype": subtype,
        "severity": severity,
        "description": description,
        "status": "ACTIVE"
    }

    incident_history.append(incident)
    save_incident(incident)

    return incident


def save_incident(incident):
    try:
        with open(HISTORY_FILE, "r") as file:
            file.read()
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "ID",
                "Timestamp",
                "Type",
                "Subtype",
                "Severity",
                "Description",
                "Status"
            ])

        writer.writerow([
            incident["id"],
            incident["timestamp"],
            incident["type"],
            incident["subtype"],
            incident["severity"],
            incident["description"],
            incident["status"]
        ])


def update_incident(incident):
    with open(HISTORY_FILE, "r", newline="") as file:
        rows = list(csv.reader(file))

    with open(HISTORY_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        for row in rows:
            if row and row[0] == incident.get("ID", incident.get("id")):
                row[6] = incident["status"]

            writer.writerow(row)

def load_incident_history():
    try:
        with open(HISTORY_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for incident in reader:
                incident_history.append(incident)

    except FileNotFoundError:
        pass

def get_incident_history():
    load_incident_history()
    return incident_history


def display_incident_history():
    print("\nINCIDENT HISTORY")
    print("-" * 50)

    if not incident_history:
        print("No incidents recorded")
        return

    for incident in incident_history:
        display_incident(incident)


def resolve_incident(incident):
    incident["status"] = "RESOLVED"
    incident["resolved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_incident(incident)


def display_incident(incident):
    print("-" * 50)
    print("INCIDENT DETAILS")
    print("-" * 50)
    print("ID:", incident["id"])
    print("Timestamp:", incident["timestamp"])
    print("Type:", incident["type"])
    print("Subtype:", incident["subtype"])
    print("Severity:", incident["severity"])
    print("Description:", incident["description"])
    print("Status:", incident["status"])

    if incident["status"] == "RESOLVED":
        print("Resolved At:", incident["resolved_at"])

    print("-" * 50)


if __name__ == "__main__":
    incident = create_incident(
        "Application",
        "CRITICAL",
        "Application returned HTTP 503",
        "HTTP"
    )

    print("\nBEFORE RECOVERY")
    display_incident(incident)

    resolve_incident(incident)

    print("\nAFTER RECOVERY")
    display_incident(incident)