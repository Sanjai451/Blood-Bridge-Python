# from flask import Flask, render_template, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sanjai%40451@localhost/lifelink_db'
# app.config['SECRET_KEY'] = 'your_secret_key'
# db = SQLAlchemy(app)

# # Models
# class BloodRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     blood_type = db.Column(db.String(10), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     priority = db.Column(db.Boolean, default=True)

# class Inventory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     blood_type = db.Column(db.String(10), nullable=False)
#     stock_level = db.Column(db.Integer, nullable=False)

# # Routes
# @app.route('/')
# def home():
#     return render_template('dashboard.html')

# @app.route('/dashboard')
# def dashboard():
#     blood_requests = BloodRequest.query.all()
#     return render_template('dashboard.html', blood_requests=blood_requests)

# @app.route('/request_blood', methods=['GET', 'POST'])
# def request_blood():
#     if request.method == 'POST':
#         blood_type = request.form.get('blood_type')
#         quantity = int(request.form.get('quantity'))
#         new_request = BloodRequest(blood_type=blood_type, quantity=quantity)
#         db.session.add(new_request)
#         db.session.commit()
#         flash('Blood request submitted!')
#         return redirect(url_for('dashboard'))
#     return render_template('request_blood.html')

# @app.route('/update_inventory', methods=['GET', 'POST'])
# def update_inventory():
#     if request.method == 'POST':
#         blood_type = request.form.get('blood_type')
#         stock_level = int(request.form.get('stock_level'))
#         inventory = Inventory.query.filter_by(blood_type=blood_type).first()
#         if inventory:
#             inventory.stock_level = stock_level
#         else:
#             new_inventory = Inventory(blood_type=blood_type, stock_level=stock_level)
#             db.session.add(new_inventory)
#         db.session.commit()
#         flash('Inventory updated!')
#         return redirect(url_for('dashboard'))
#     return render_template('update_inventory.html')

# # Run the application
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sanjai%40451@localhost/lifelink_db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Models
class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Boolean, default=True)
    requestor_type = db.Column(db.String(20), nullable=False)  # Add type to identify acceptor


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    stock_level = db.Column(db.Integer, nullable=False)

class BloodDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)  # Add address field


# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    blood_requests = BloodRequest.query.all()
    donors = BloodDonation.query.all()  # Fetch all donors
    return render_template('dashboard.html', blood_requests=blood_requests, donors=donors)


@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        quantity = int(request.form.get('quantity'))
        requestor_type = request.form.get('requestor_type')  # Ensure this retrieves the value from the form
        
        # Check if requestor_type is None or empty
        if not requestor_type:
            flash('Requestor type is required.')
            return redirect(url_for('request_blood'))
        
        new_request = BloodRequest(blood_type=blood_type, quantity=quantity, requestor_type=requestor_type)
        db.session.add(new_request)
        db.session.commit()
        flash('Blood request submitted!')
        return redirect(url_for('dashboard'))
    return render_template('request_blood.html')



@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        stock_level = int(request.form.get('stock_level'))
        inventory = Inventory.query.filter_by(blood_type=blood_type).first()
        if inventory:
            inventory.stock_level = stock_level
        else:
            new_inventory = Inventory(blood_type=blood_type, stock_level=stock_level)
            db.session.add(new_inventory)
        db.session.commit()
        flash('Inventory updated!')
        return redirect(url_for('dashboard'))
    return render_template('update_inventory.html')


@app.route('/donate_blood', methods=['GET', 'POST'])
def donate_blood():
    if request.method == 'POST':
        donor_name = request.form.get('donor_name')
        blood_type = request.form.get('blood_type')
        contact_info = request.form.get('contact_info')
        address = request.form.get('address')  # Get address from the form
        new_donor = BloodDonation(donor_name=donor_name, blood_type=blood_type, contact_info=contact_info, address=address)
        db.session.add(new_donor)
        db.session.commit()
        flash('Donor information submitted!')
        return redirect(url_for('dashboard'))
    return render_template('donate_blood.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
