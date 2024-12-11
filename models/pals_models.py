import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
from flask import flash, session, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler

current_time = datetime.utcnow()#get current time and date

class PAls():
	def __init__(self, card_num, card_code, messege, comments, created_at):
		self.card_num = card_num
		self.card_code = card_code
		self.messege = messege
		self.comments = comments
		self.created_at = created_at
        
	def add(self):
		try:
			conn = sqlite3.connect('Digital_read.db')
			cur = conn.cursor()
			cur.execute(""" CREATE TABLE if not exists Palsdb(
	                               Id INTEGER PRIMARY KEY AUTOINCREMENT,
	                               Card_num TEXT,
								   Card_code TEXT,
								   Messege TEXT,
								   Comments TEXT,
								   Created_at DATETIME
	                               )""")
			data = [self.card_num, self.card_code, self.messege, self.comments, self.created_at]
			cur.execute(""" 
	                                INSERT INTO Palsdb(Card_num, Card_code, Messege, Comments, Created_at) VALUES(?,?,?,?,?)
	            """, data)
			conn.commit()
			conn.close()
			flash("New messege, Pal")
		except Error as e:
			flash(f"⚠An Error occured: {e}")  
            
	def drop(self):
		try:
			conn = sqlite3.connect('Digital_read.db')
			cur = conn.cursor()
			cur.execute(''' DROP TABLE Palsdb ''')
			conn.commit()
			conn.close()
		except Error as e:
			flash(f"⚠An Error occured: {e}")  
    
	def show(self):
		try:
			conn = sqlite3.connect('Digital_read.db')
			cur = conn.cursor()
			cur.execute(""" CREATE TABLE if not exists Palsdb (
	                               Id INTEGER PRIMARY KEY AUTOINCREMENT,
	                               Card_num TEXT,
								   Card_code TEXT,
								   Messege TEXT,
								   Comments TEXT,
								   Created_at DATETIME
	                               )""")
					
	        #check for objects older than 2 weeks
			two_weeks_ago = current_time - timedelta(weeks=2)
	        
			info = conn.execute(""" 
	                                    SELECT *  
										FROM Palsdb
										WHERE Created_at > ?  
										ORDER BY Id DESC
	                                    """,(two_weeks_ago,))      
			results = info.fetchall()
			return results
			
			conn.commit()
			conn.close()
		except Error as e:
			flash(f"⚠An Error occured: {e}")  
        
     #Delete a messege when the cardnum and cardcode are the same as those in session
	def delete_messege_from_database(self, session_card_num, session_card_code):
		session_card_num = session.get('card_num')
		session_card_code = session.get('card_code')
		try:
			conn = sqlite3.connect('Digital_read.db')
			cur = conn.cursor()
			cur.execute(""" 
	        				DELETE FROM Palsdb WHERE card_num = ? and card_code = ?
							""",(session_card_num,session_card_code))
			flash("You deleted a messege")
			conn.commit()
			conn.close()
			flash('A pal deleted a messege.')
		except Error as e:
			flash(f"⚠An Error occured: {e}")  
