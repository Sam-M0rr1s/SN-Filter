valid_prefixes = ["PB", "PF", "PW", "PC"]

def get_serial_number():
    #returns serial from scan or types in manual one
    while True:
        raw_scan = input("please scan the serial number (or type 'manual'): ")

        if raw_scan.lower() == "manual":
            return None

        if raw_scan.lower() == "export":
            return "export"

        raw_scan = raw_scan.upper()

        if not raw_scan.startswith("1S"):
            print("Serial number is invalid")
            continue

        start_index = -1
        for prefix in valid_prefixes:
            if prefix in raw_scan:
                start_index = raw_scan.find(prefix)
                break

        if start_index == -1:
            print("Serial number does not contain a recognised Lenovo info")
            continue

        return raw_scan[start_index:start_index + 8]


def get_manual_serial():
    #collects serial and puts it in upper case
    return input("Enter serial number: ").strip().upper()


def get_manual_details():
    #fallback for if api fails
    make = input("Enter device make: ").strip().title()
    model = input("Enter device model: ").strip().title()
    return make, model

def export_table(current_batch):
    table = input("Export current table, or a different one? (current/other): ").strip().lower()
    if table == "other":
        return input("Enter the table name to export: ").strip()
    return current_batch





