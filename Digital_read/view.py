from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from models.view_models import cleanup_online_tb
from settings import Config
from Digital_read.card_stock import magazine_stocks, math_stocks

view_bp = Blueprint('view_bp', __name__, template_folder='templates/digital_read', static_folder='static')


@view_bp.route('/')
@view_bp.route('/view')
def View():
    title="view"
    active_cardnum = session.get('card_num')  # Extract card number from session
    active_cardcode = session.get('card_code')  # Extract card code from session
    
    #return render_template('view.html', title=title)
    cleanup_online_tb()
    if 'card_num' and 'card_code' in session:
    	if active_cardnum in magazine_stocks and magazine_stocks[active_cardnum]== active_cardcode:
    		flash("Welcome to the digital magazine!")
    		return render_template('view.html', title=title)
    	else:
    		flash("Unknown card!")
    		return redirect(url_for('authorisation_bp.Authorisation'))
    else:
    	flash('🚫Please login!!')
    	return redirect(url_for('authorisation_bp.Authorisation'))
