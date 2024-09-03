import secrets
import random
from models.view_models import CArds

class Config():
	SECRET_KEY = secrets.token_hex(4020)
	DEBUG = True
	#DATABASE_URI
	name="digital read"
	email="digitalread@gmail.com"
	password="test"
	RECAPTCHA_PUBLIC_KEY = "6Lf9j20pAAAAAKTR5MBCGeF6VgPyxguYV0jXjEqD"
	RECAPTCHA_PRIVATE_KEY = "6Lf9j20pAAAAAIe5oVo8cG4w7SUSCPHQgPuqKVYy"
	host='0.0.0.0' 
	port=9000
	cards=CArds("0","1","2")
	

def generate_password(quantity, randomly=random.randint(7,13)):
	many = range(quantity)
	for card in many:
		card_number=secrets.token_hex(randomly)
		card_code=secrets.token_hex(3)
		print(f"'{card_number}':'{card_code}',")
#generate_password(1000)
