from datetime import datetime

incident_history = []
incident_counter = 0


def create_incident(incident_type, severity, description):
    global incident_counter
    incident_counter += 1

    incident = {
        "id": "INC-" + datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(incident_counter),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": incident_type,
        "severity": severity,
        "description": description,
        "status": "ACTIVE"
    }

    incident_history.append(incident)

    return incident
def get_incident_history():
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


def display_incident(incident):
    print("-" * 50)
    print("INCIDENT DETAILS")
    print("-" * 50)
    print("ID:", incident["id"])
    print("Timestamp:", incident["timestamp"])
    print("Type:", incident["type"])
    print("Severity:", incident["severity"])
    print("Description:", incident["description"])
    print("Status:", incident["status"])

    if incident["status"] == "RESOLVED":
        print("Resolved At:", incident["resolved_at"])

    print("-" * 50)


if __name__ == "__main__":
    incident1 = create_incident(
        "Application",
        "CRITICAL",
        "Application returned HTTP 503"
    )

    incident2 = create_incident(
        "Resource",
        "WARNING",
        "High memory usage detected"
    )

    display_incident_history()