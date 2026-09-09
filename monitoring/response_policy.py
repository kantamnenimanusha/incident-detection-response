def get_response(incident_type, severity):
    if incident_type == "Application" and severity == "CRITICAL":
        return "RESTART_APPLICATION"

    if incident_type == "Resource" and severity == "WARNING":
        return "MONITOR_AND_LOG"

    return "NO_ACTION"


if __name__ == "__main__":

    response = get_response(
        "Application",
        "CRITICAL"
    )

    print("Recommended Response:", response)