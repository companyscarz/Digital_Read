from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from settings import Config

signup_bp = Blueprint('signup_bp', __name__, template_folder='templates/digital_read', static_folder='static')

@signup_bp.route('/signup')
def Signup():
    title="signup"
    return render_template('signup.html', title=title)