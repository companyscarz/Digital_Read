from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from Digital_read.forms import Verification 
from datetime import datetime
from settings import Config
from models.view_models import CArds

authorisation_bp = Blueprint('authorisation_bp', __name__, template_folder='templates/digital_read', static_folder='static')

@authorisation_bp.route('/authorisation', methods=['GET', 'POST'])
def Authorisation():
    title="authorisation"
    form = Verification()
    current_time = datetime.utcnow()#get current time
    if form.validate_on_submit():
    	#check if the card number is in the list of card numbers... 
    	#this ensures only specific cards can continue..
    	#then check if card is on online_tb so that only one person can use it
    	# then continue to look for... 
    	data = CArds(form.card_number.data, form.password.data, current_time)
    	data.Look_up()
    	#the Look_up function checks if the card number is in the database 
    	#if true then saves the card number and password as sesions and adds the card to online table
    	#if not in db then it adds on the cards db and then adds the card to online table and saves the card and password on session
    	return redirect(url_for('view_bp.View'))
    else:
    	return render_template('authorisation.html', title=title, form=form)
    	flash('Please fill in the fields correctly!!')
