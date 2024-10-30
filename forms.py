from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Login')

class BloodRequestForm(FlaskForm):
    blood_type = StringField('Blood Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

class DonationScheduleForm(FlaskForm):
    submit = SubmitField('Schedule Donation')

class InventoryUpdateForm(FlaskForm):
    blood_type = StringField('Blood Type', validators=[DataRequired()])
    stock_level = IntegerField('Stock Level', validators=[DataRequired()])
    submit = SubmitField('Update Inventory')


