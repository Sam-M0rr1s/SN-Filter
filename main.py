from SN_filter import get_serial_number, get_manual_serial, get_manual_details, export_table
from device_type import get_warranty_info
from database import save_serial
from export import export_batch

batch_name = input("Enter table name: ").strip()

def process_serial(serial):
    result = get_warranty_info(serial)
    info = result.get("data")

    if not info:
        print(f"No warranty info found for {serial} on Lenovo's system.")
        make, model = get_manual_details()
        save_serial(batch_name, serial, make=make, model=model)
        return

    machine = info["machineInfo"]
    warranty = info["currentWarranty"]

    print("Model:", machine["productName"])
    print("Warranty status:", info["warrantyStatus"])
    print("Days remaining:", warranty["remainingDays"])

    save_serial(
        batch_name, serial,
        make="Lenovo",
        model=machine["productName"],
        warranty_status=info["warrantyStatus"],
        warranty_end_date=warranty["endDate"],
        days_remaining=warranty["remainingDays"]
    )

while True:
    serial = get_serial_number()

    if serial == "export":
        target = export_table(batch_name)
        export_batch(target)
        continue

    if serial is None:
        serial = get_manual_serial()

    process_serial(serial)