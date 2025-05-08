from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from settings import Config

admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__, template_folder='templates/digital_read', static_folder='static')

@admin_dashboard_bp.route('/admin_dashboard')
def Admin_dashboard():
    title="admin_dashboard" #probably get the active admin name from database and use it as the title 
    return render_template('admin_dashboard.html', title=title)