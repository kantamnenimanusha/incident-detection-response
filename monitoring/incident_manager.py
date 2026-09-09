from datetime import datetime


def create_incident(incident_type, severity, description):
    incident = {
        "id": "INC-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": incident_type,
        "severity": severity,
        "description": description,
        "status": "ACTIVE"
    }

    return incident


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

    incident = create_incident(
        "Application",
        "CRITICAL",
        "Application returned HTTP 503"
    )

    print("Before Recovery:")
    display_incident(incident)

    resolve_incident(incident)

    print("After Recovery:")
    display_incident(incident)