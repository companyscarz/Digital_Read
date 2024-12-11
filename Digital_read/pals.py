from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from datetime import datetime
from settings import Config
from models.pals_models import PAls
from Digital_read.forms import Pals_Form

pals_bp = Blueprint('pals_bp', __name__, template_folder='templates/digital_read', static_folder='static')

sent_messeges = Config.pals

@pals_bp.route('/pals', methods=['POST','GET'])
def Pals():
	title="Pals"
	active_cardnum = session.get('card_num')  # Extract card number from session
	active_cardcode = session.get('card_code')  # Extract card code from session
	Created_at = datetime.utcnow()#get current time
	form = Pals_Form()
	
    #return render_template('view.html', title=title)
	if 'card_num' and 'card_code' in session:
		if form.validate_on_submit():
			data=PAls('Card_num', 'Card_code', form.text.data, 'Comments', Created_at)
			data.add()
			flash('Messege has been sent to Pals')
			return render_template('pals.html', sent_messeges=sent_messeges.show(), cardnum_in_session=active_cardnum, cardcode_in_session=active_cardcode ,form=form)#reload pals page and show messeges
		return render_template('pals.html', sent_messeges=sent_messeges.show(), cardnum_in_session=active_cardnum, cardcode_in_session=active_cardcode ,form=form)#reload pals page and show messeges
	
	else:
		flash('🚫Please login!!')
		return redirect(url_for('authorisation_bp.Authorisation'))
