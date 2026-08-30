from SN_filter import get_serial_number
from device_type import get_warranty_info
from database import create_database, save_serial

create_database()

while True:
    serial = get_serial_number()
    data = get_warranty_info(serial)

    info = data["data"]
    machine = info["machineInfo"]
    warranty = info["currentWarranty"]

    print("Model:", machine["productName"])
    print("Serial:", machine["serial"])
    print("Warranty status:", info["warrantyStatus"])
    print("Warranty end date:", warranty["endDate"])
    print("Days remaining:", warranty["remainingDays"])

    save_serial(
        serial,
        model=machine["productName"],
        warranty_status=info["warrantyStatus"],
        warranty_end_date=warranty["endDate"],
        days_remaining=warranty["remainingDays"]
    )