from flask_sqlalchemy import SQLAlchemy
from os import path
from flask import Flask
from SN_filter import get_serial_number  

app = Flask(__name__)
db_name = "serial_numbers.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def create_database():
    if not path.exists(db_name):
        with app.app_context():
            db.create_all()
        print('Created Database!')



class SerialNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(20), unique=True, nullable=False)
    warranty_status = db.Column(db.String(50))
    warranty_end_date = db.Column(db.String(20))
    days_remaining = db.Column(db.Integer)


def save_serial(serial, model=None, warranty_status=None, warranty_end_date=None, days_remaining=None):
    with app.app_context():
        existing = SerialNumber.query.filter_by(serial_number=serial).first()

        if existing:
            existing.model = model
            existing.warranty_status = warranty_status
            existing.warranty_end_date = warranty_end_date
            existing.days_remaining = days_remaining
            db.session.commit()
            print(f"Updated {serial} in database")
        else:
            entry = SerialNumber(
                serial_number=serial,
                model=model,
                warranty_status=warranty_status,
                warranty_end_date=warranty_end_date,
                days_remaining=days_remaining
            )
            db.session.add(entry)
            db.session.commit()
            print(f"Saved {serial} to database")


if __name__ == "__main__":
    create_database()
    while True:
        serial = get_serial_number()
        save_serial(serial)

