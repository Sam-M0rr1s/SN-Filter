import csv
import os
from database import db, app, get_table, sanitize_table_name

OUTPUT_DIR = "exports"

def get_rows(batch_name):
    table = get_table(batch_name)
    with app.app_context():
        with db.engine.connect() as conn:
            result = conn.execute(table.select())
            rows = [dict(row._mapping) for row in result]
    return rows

def _action_for_make(make):
    if make in ("Lenovo", "Microsoft"):
        return "Blanco"
    return "Physical Destruction"

def export_batch(batch_name):
    rows = get_rows(batch_name)

    if not rows:
        print(f"No data found for table '{batch_name}' - nothing to export")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = sanitize_table_name(batch_name)

    full_path = os.path.join(OUTPUT_DIR, f"{safe_name}_full.csv")
    fieldnames = ["id", "make", "model", "serial_number", "warranty_status", "warranty_end_date", "days_remaining"]
    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    serials_path = os.path.join(OUTPUT_DIR, f"bulkremoval.csv")
    with open(serials_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["serial number"])
        for row in rows:
            writer.writerow([row["serial_number"]])

    action_path = os.path.join(OUTPUT_DIR, f"{safe_name}_action.csv")
    with open(action_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["make", "model", "serial_number", "action"])
        for row in rows:
            action = _action_for_make(row["make"])
            writer.writerow([row["make"], row["model"], row["serial_number"], action])

    print(f"Exported {len(rows)} devices from '{batch_name}':")
    print(f"  Full data:      {full_path}")
    print(f"  Serials only:   {serials_path}")
    print(f"  Action list:    {action_path}")