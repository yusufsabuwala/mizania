from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()
current_time_est = datetime.now(ZoneInfo("America/New_York"))


class Spending(db.Model):
    __tablename__ = 'spending'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)  # New column for details
    payment_method = db.Column(db.String(50), nullable=True)  # New column for payment method
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Spending {self.id} - ${self.amount} on {self.date}>'
