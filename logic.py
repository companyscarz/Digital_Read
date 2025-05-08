from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from settings import Config
from login import Login
from signup import Signup
from scholar_dashboard import Scholar_dashboard
from admin_dashboard import Admin_dashboard

#this is the control center of the project

def generate_password(quantity, randomly=random.randint(7,13)):
	many = range(quantity)
	for card in many:
		card_number=secrets.token_hex(randomly)
		card_code=secrets.token_hex(3)
		print(f"'{card_number}':'{card_code}',")
		
generate_password(1000)
#Config.pals.add()
#Print the messages 
#data=Config.pals.show()
#for info in data:
#	print(info)