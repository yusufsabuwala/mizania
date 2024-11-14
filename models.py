from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()
current_time_est = datetime.now(ZoneInfo("America/New_York"))

class Person(db.Model):
    __tablename__ = 'person'
    #dcid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thali_number = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)  # Keep thali_number as unique identifier
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    #active_status = db.Column(db.Boolean, default=True)

    # Relationship with Transaction
    transactions = db.relationship('Transaction', backref='person', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    dcid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thali_number = db.Column(db.Integer, db.ForeignKey('person.thali_number'), nullable=False)  # Updated to reference thali_number
    total_amount = db.Column(db.Float, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)  # Added field
    last_name = db.Column(db.String(100), nullable=False)   # Added field
    transaction_date = db.Column(db.DateTime, default=current_time_est)

class Spending(db.Model):
    __tablename__ = 'spending'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)  # New column for details
    payment_method = db.Column(db.String(50), nullable=True)  # New column for payment method
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Spending {self.id} - ${self.amount} on {self.date}>'
