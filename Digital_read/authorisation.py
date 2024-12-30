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
        #if form.card_number.data in magazine_stocks and magazine_stocks[form.card_number.data]== form.password.data:
    	data = CArds(form.card_number.data, form.password.data, current_time)
    	data.Look_up()
    	return redirect(url_for("view_bp.View")
    else:
    	flash('Please fill in the fields correctly!!')
    	return render_template('authorisation.html', title=title, form=form)
