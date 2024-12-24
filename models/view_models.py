from datetime import datetime, timedelta
from flask import flash, session, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from delicate import connection
import webbrowser

current_time = datetime.utcnow()
connections = connection

def cleanup_online_tb():
    try:
        #get the session data and delete it if its 30 minutes
        relax_time = (current_time - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S') 
        conn = connections
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE if not exists online_tb (
		                               Id SERIAL PRIMARY KEY,
		                               Card_num VARCHAR (20) NOT NULL,
		                               Created_at DATETIME
		                               )""")
        cur.execute(""" DELETE FROM online_tb WHERE Created_at <? """,(relax_time,))
        conn.commit() 
        conn.close()
        print("online_tb Cleared")
        #if there is an error in the database then flash a message
    except Error as e:
        conn.commit()
        conn.close()


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_online_tb, 'interval', hours=1)
scheduler.start()

#during expansion add  account table and link it to the card table. 
#on the card table you will add columns of pdf 
#Digital_read database
class CArds():
    def __init__(self, card_num, card_code, created_at):
        self.card_num = card_num
        self.card_code = card_code
        self.created_at = created_at   
        	                                              
    def Look_up(self):
        try: 
        #check online_tb if card is there then flash card is in use 
        #if card is not there then proceed to other authorisation steps
            conn = connections
            cur = conn.cursor()
            cur.execute(""" CREATE TABLE if not exists online_tb (
		                               Id SERIAL PRIMARY KEY,
		                               Card_num VARCHAR (20) NOT NULL,
		                               Created_at DATETIME
		                               )""")  
            
            #query to check if card exists in the online table
            cur.execute("""SELECT * FROM online_tb WHERE Card_num = ?""", (self.card_num,))
            # query to get card if the card_num exists 
            card_online = cur.fetchone()
            if card_online:
            	flash("This card is currently in use!")
            else:
	            #check for objects older than 9 weeks 
	            nine_weeks_ago = (current_time - timedelta(weeks=9)).strftime('%Y-%m-%d %H:%M:%S')
				
	            #make connections 
	            conn = connections
	            cur = conn.cursor()
	            cur.execute(""" CREATE TABLE if not exists card_db (
		                               Id SERIAL PRIMARY KEY,
		                               Card_num VARCHAR (20) NOT NULL,
		                               Card_code VARCHAR (20) NOT NULL, 
		                               Created_at DATETIME
		                               )""")
		       
	            #query to check if card exists but if the date created is older than 9 weeks this one should not be allowed
	            cur.execute("""SELECT * FROM card_db WHERE Card_num = ? AND Created_at < ?""", (self.card_num,nine_weeks_ago))                        
		   	# query to check if the card_num exists and not check expiry
	            expired_card = cur.fetchone()
	            
	            # if the card is older than 15 weeks then dont allow in any enty 
	            if expired_card :
	            	flash("Sorry, this card is expired!")
	            else:
	            	# Check if the card is valid (not expired)
	            	cur.execute("""SELECT * FROM card_db WHERE Card_num = ? AND Card_code = ?""", (self.card_num, self.card_code))
	            	valid_card = cur.fetchone()     	
		            #when card is registered then save in session, continue to view page then save on online_tb
	            	if valid_card: # when a result is found 
		            	session['card_num']=self.card_num
		            	session['card_code']=self.card_code
		            	#after saving on session then add the card_num to online_tb
		            	cur.execute(""" CREATE TABLE if not exists online_tb (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num VARCHAR (20) NOT NULL,
			                               Created_at DATETIME
			                               )""")
		            	data = [self.card_num, self.created_at]
		            	cur.execute(""" 
			                                	INSERT INTO online_tb(Card_num,Created_at) VALUES(?,?)
			            				""", data)
		            	flash("Welcome back to Digital read")
		            	
		            #if card is not registered then save it on cards data base
	            	else: 
		            	cur.execute(""" CREATE TABLE if not exists card_db (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num VARCHAR (20) NOT NULL,
			                               Card_code VARCHAR (20) NOT NULL, 
			                               Created_at DATETIME
			                               )""")
		            	data = [self.card_num, self.card_code, self.created_at]
		            	#register the card on the card_db
		            	cur.execute(""" 
			                                	INSERT INTO card_db(Card_num, Card_code, created_at) VALUES(?,?,?)
			            				""", data)
			            				
			        #add the card on the online table and save on session
		            	session['card_num']=self.card_num
		            	session['card_code']=self.card_code
		            	#after saving on session then add the card_num to online_tb
		            	cur.execute(""" CREATE TABLE if not exists online_tb (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num VARCHAR (20) NOT NULL,
			                               Created_at DATETIME
			                               )""")
		            	data = [self.card_num, self.created_at]
		            	cur.execute(""" 
			                                	INSERT INTO online_tb(Card_num, Created_at) VALUES(?,?)
			            				""", data) 
			            				
		            	flash("Enjoy your say on Digital read.")
		            	#welcome the user          		
			        #commit and save the changes and save changes
       							         
            conn.commit() 
            conn.close() 
		            #if there is an error in the database then flash a message
        except Error as e:
        	conn.commit()
        	conn.close()
        	flash(f"⚠An Error occured{e}") 
