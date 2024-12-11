from flask import Flask
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

#secret key
app.config["SECRET_KEY"]
#config for recaptcha
app.config["RECAPTCHA_PUBLIC_KEY"]
app.config["RECAPTCHA_PRIVATE_KEY"] 

from Digital_read.authorisation import authorisation_bp
from Digital_read.view import view_bp
from Digital_read.pals import pals_bp

app.register_blueprint(view_bp)
app.register_blueprint(authorisation_bp)
app.register_blueprint(pals_bp)

if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], port=Config.port, host=Config.host)
