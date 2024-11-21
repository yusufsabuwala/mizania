from flask import Flask, request, render_template, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
from io import StringIO
#from models import Spending

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fmb_fi.db'  # Path to your SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
current_time_est = datetime.now(ZoneInfo("America/New_York"))

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create the database tables
with app.app_context():
    db.create_all()

'''
run this in terminal to drop and create db tables
from app import db, app
with app.app_context():
    db.drop_all()
    db.create_all()

'''



# Route to render the landing page
@app.route('/')
def index():
    return render_template('index.html')


''' BUDGET APP'''
# Define the Spending model if not already defined in models.py

class Spending(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)  # New column for details
    payment_method = db.Column(db.String(50), nullable=True)  # New column for payment method
    date = db.Column(db.DateTime, default=current_time_est)


# Route to render the spending page and display all current month entries
@app.route('/budget', methods=['GET'])
def track_spending_page():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    total_spending = db.session.query(db.func.sum(Spending.amount)).filter(
        db.extract('month', Spending.date) == current_month,
        db.extract('year', Spending.date) == current_year
    ).scalar() or 0  # Default to 0 if no data

    # Fetch all entries for the current month
    spending_entries = Spending.query.filter(
        db.extract('month', Spending.date) == current_month,
        db.extract('year', Spending.date) == current_year
    ).all()

    return render_template('budget.html', total_spending=total_spending, spending_entries=spending_entries)

# Route to handle adding a new spending entry
@app.route('/add_spending', methods=['POST'])
def add_spending():
    data = request.json
    new_spending = Spending(amount=data['amount'],description=data['description'],payment_method=data['payment_method'])
    db.session.add(new_spending)
    db.session.commit()
    return jsonify({'message': 'Spending entry added successfully!'}), 201

# Route to edit a spending entry
@app.route('/edit_spending/<int:id>', methods=['PUT'])
def edit_spending(id):
    data = request.json
    spending_entry = Spending.query.get(id)
    if spending_entry:
        spending_entry.amount = data['amount']
        spending_entry.description = data['description']
        spending_entry.payment_method = data['payment_method']
        db.session.commit()
        return jsonify({'message': 'Spending entry updated successfully!'}), 200
    else:
        return jsonify({'error': 'Spending entry not found'}), 404

# Route to delete a spending entry by ID
@app.route('/delete_spending/<int:id>', methods=['DELETE'])
def delete_spending(id):
    spending_entry = Spending.query.get(id)
    if spending_entry:
        db.session.delete(spending_entry)
        db.session.commit()
        return jsonify({'message': 'Spending entry deleted successfully!'}), 200
    else:
        return jsonify({'error': 'Spending entry not found'}), 404


@app.route('/download_csv', methods=['GET'])
#@login_required  # Optional: remove if download should be public
def download_csv():
    # Create a StringIO object to write CSV data
    output = StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow(['ID', 'Amount', 'Description', 'Payment Method', 'Date'])

    # Query all spending entries
    spending_entries = Spending.query.all()

    # Write data rows
    for entry in spending_entries:
        writer.writerow([entry.id, entry.amount, entry.description, entry.payment_method, entry.date.strftime('%Y-%m-%d %H:%M:%S')])

    # Create a Response object and set headers
    output.seek(0)
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=spending_data.csv'

    return response
#######################################################



# Do not delete this

if __name__ == '__main__':
    app.run(debug=True)