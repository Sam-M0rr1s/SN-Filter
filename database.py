from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import re

app = Flask(__name__)
db_name = "serial_numbers.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def sanitize_table_name(batch_name):
    #Turns a human typed name and turns it a name for a table
    name = batch_name.strip().lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)   # anything not a letter or number becomes _
    return f"batch_{name}"


def get_table(batch_name):
    #Returns the table name and creates it if it doesnt exist
    table_name = sanitize_table_name(batch_name)

    # Reuse the table definition if its already built it this run
    if table_name in db.metadata.tables:
        table = db.metadata.tables[table_name]
    else:
        table = db.Table(
            table_name,
            db.metadata,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('make', db.String(50)),
            db.Column('model', db.String(100)),
            db.Column('serial_number', db.String(20), unique=True, nullable=False),
            db.Column('warranty_status', db.String(50)),
            db.Column('warranty_end_date', db.String(20)),
            db.Column('days_remaining', db.Integer),
        )

    with app.app_context():
        table.create(db.engine, checkfirst=True)   # only creates it if it doesn't already exist

    return table


def save_serial(batch_name, serial, make=None, model=None, warranty_status=None, warranty_end_date=None, days_remaining=None):
    table = get_table(batch_name)

    with app.app_context():
        with db.engine.connect() as conn:
            existing = conn.execute(
                table.select().where(table.c.serial_number == serial)
            ).first()

            if existing:
                conn.execute(
                    table.update()
                    .where(table.c.serial_number == serial)
                    .values(make=make, model=model, warranty_status=warranty_status,
                            warranty_end_date=warranty_end_date, days_remaining=days_remaining)
                )
                conn.commit()
                print(f"Updated {serial} in '{batch_name}'")
            else:
                conn.execute(
                    table.insert().values(
                        serial_number=serial, make=make, model=model,
                        warranty_status=warranty_status, warranty_end_date=warranty_end_date,
                        days_remaining=days_remaining
                    )
                )
                conn.commit()
                print(f"Saved {serial} to '{batch_name}'")

