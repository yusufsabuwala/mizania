from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fmb_fi.db'  # Path to your SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
#migrate = Migrate(app, db)

# Define the Person model
class Person(db.Model):
    #dcid = db.Column(db.String, primary_key=True)
    thali_number = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

# Define the Transaction model
class Transaction(db.Model):
    dcid = db.Column(db.Integer, primary_key=True)
    thali_number = db.Column(db.String, db.ForeignKey('person.thali_number'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

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


# Route to render the add_person.html page (handles GET requests)
# @app.route('/add_person', methods=['GET'])
# def add_person_page():
#     return render_template('add_person.html')


# Route to handle form submission and add a person to the database (handles POST requests)
@app.route('/submit_person', methods=['POST'])
def submit_person():
    data = request.json  # Expects JSON data
    new_person = Person(
        thali_number=data['thali_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data['phone_number']
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person added successfully!'}), 201

# Route to render the add_person.html page
@app.route('/add_person', methods=['GET'])
def add_person_page():
    people = Person.query.all()  # Fetch all Person records
    return render_template('add_person.html', people=people)

# Route to delete a person by thali_number
@app.route('/delete_person/<thali_number>', methods=['DELETE'])
def delete_person(thali_number):
    person = Person.query.filter_by(thali_number=thali_number).first()
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted successfully!'}), 200
    else:
        return jsonify({'error': 'Person not found'}), 404



''' TRANSACTIONS'''

# Route to render the add_transaction.html page (handles GET requests)
@app.route('/add_transaction', methods=['GET'])
def add_transaction_page():
    return render_template('add_transaction.html')  # Create a new HTML template for adding a transaction

# Route to handle form submission and add a transaction to the database (handles POST requests)
@app.route('/submit_transaction', methods=['POST'])
def submit_transaction():
    data = request.json
    
    # Check if the thali_number exists in the Person table
    person = Person.query.filter_by(thali_number=data['thali_number']).first()
    if not person:
        # Return an error message if the thali_number does not exist
        return jsonify({'error': 'Thali number does not exist. Please add the person first.'}), 400
    
    # If thali_number exists, create and store the transaction
    new_transaction = Transaction(
        thali_number=data['thali_number'],
        total_amount=data['total_amount'],
        first_name=person.first_name,  # Populate from existing person data
        last_name=person.last_name
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully!'}), 201


# Route to view all transactions
@app.route('/transactions')
def view_transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
