import csv

HISTORY_FILE = "logs/incident_history.csv"


def display_history():
    print("\nINCIDENT HISTORY")
    print("=" * 60)

    try:
        with open(HISTORY_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for incident in reader:
                print("ID:", incident["ID"])
                print("Timestamp:", incident["Timestamp"])
                print("Type:", incident["Type"])
                print("Severity:", incident["Severity"])
                print("Description:", incident["Description"])
                print("Status:", incident["Status"])
                print("-" * 60)

    except FileNotFoundError:
        print("No incident history found.")


if __name__ == "__main__":
    display_history()