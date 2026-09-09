import csv

HISTORY_FILE = "logs/incident_history.csv"


def display_history():
    print("\nINCIDENT HISTORY")
    print("-" * 60)

    try:
        with open(HISTORY_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            incidents = list(reader)

            if not incidents:
                print("No incidents recorded")
                return

            for incident in incidents:
                print("ID:", incident["ID"])
                print("Timestamp:", incident["Timestamp"])
                print("Type:", incident["Type"])
                print("Subtype:", incident["Subtype"])
                print("Severity:", incident["Severity"])
                print("Description:", incident["Description"])
                print("Status:", incident["Status"])
                print("-" * 60)

    except FileNotFoundError:
        print("Incident history file not found")


if __name__ == "__main__":
    display_history()