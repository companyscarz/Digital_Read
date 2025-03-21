from flask import Flask
from settings import Config
from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser
from models.view_models import cleanup_online_tb

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

#secret key
app.config["SECRET_KEY"]
#config for recaptcha
app.config["RECAPTCHA_PUBLIC_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] 

from Digital_read.authorisation import authorisation_bp
from Digital_read.view import view_bp
from Digital_read.pals import pals_bp


app.register_blueprint(authorisation_bp)
app.register_blueprint(view_bp)
app.register_blueprint(pals_bp)

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_online_tb, 'interval', minutes=5)
scheduler.start()

if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], port=Config.port, host=Config.host)
