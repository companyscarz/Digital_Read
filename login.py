from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from settings import Config

login_bp = Blueprint('login_bp', __name__, template_folder='templates/digital_read', static_folder='static')

@login_bp.route('/login')
def Login():
    title="login"
    return render_template('login.html', title=title)