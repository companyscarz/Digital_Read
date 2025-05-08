from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from settings import Config

scholar_dashboard_bp = Blueprint('scholar_dashboard_bp', __name__, template_folder='templates/digital_read', static_folder='static')

@scholar_dashboard_bp.route('/scholar_dashboard')
def Scholar_dashboard():
    title="scholar_dashboard" #probably get the active scholars name from database and use it as the title 
    return render_template('scholar_dashboard.html', title=title)