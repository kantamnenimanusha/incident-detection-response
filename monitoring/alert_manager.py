def send_alert(incident):
    print("\n" + "!" * 60)
    print("🚨 INCIDENT ALERT 🚨")
    print("!" * 60)
    print("Incident ID:", incident["id"])
    print("Type:", incident["type"])
    print("Subtype:", incident["subtype"])
    print("Severity:", incident["severity"])
    print("Description:", incident["description"])
    print("Status:", incident["status"])
    print("!" * 60)


if __name__ == "__main__":
    test_incident = {
        "id": "INC-TEST-001",
        "type": "Application",
        "subtype": "HTTP",
        "severity": "CRITICAL",
        "description": "Application returned HTTP 503",
        "status": "ACTIVE"
    }

    send_alert(test_incident)