from datetime import datetime, timedelta
from flask import flash, session, redirect, url_for
import pg8000
from delicate import connection

current_time = datetime.utcnow()
connections = connection


def cleanup_online_tb():
    try:
        #get the session data and delete it if its 40 minutes
        relax_time = (current_time - timedelta(minutes=40)).strftime('%Y-%m-%d %H:%M:%S') 
        conn = connections
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE if not exists online_tb (
		                               Id SERIAL PRIMARY KEY,
		                               Card_num TEXT,
		                               Created_at TIMESTAMP
		                               )""")
        cur.execute("""SELECT * FROM online_tb""")
        cur.execute("""DELETE FROM online_tb WHERE Created_at > %s""", (relax_time,))
        conn.commit()
        webbrowser.open_new_tab("https://digital-library-efaeaea2dad4.herokuapp.com/authorisation")
        #if there is an error in the database then flash a message
    except Exception as e:
        print(f"⚠An Error occured{e}")
    finally:
        pass


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
		                               Card_num TEXT,
		                               Created_at TIMESTAMP
		                               )""")  
            
            #query to check if card exists in the online table
            cur.execute("""SELECT * FROM online_tb""")
            cur.execute("""SELECT * FROM online_tb WHERE Card_num = %s""", (self.card_num,))
            # query to get card if the card_num exists 
            card_online = cur.fetchone()
            if card_online:
            	flash("This card is currently in use!")
            else:
	            #check for objects older than 1 month + bonus week--> 5 weeks
	            nine_weeks_ago = (current_time - timedelta(weeks=4)).strftime('%Y-%m-%d %H:%M:%S')
				
	            #make connections 
	            conn = connections
	            cur = conn.cursor()
	            cur.execute(""" CREATE TABLE if not exists card_db (
		                               Id SERIAL PRIMARY KEY,
		                               Card_num TEXT,
		                               Card_code TEXT, 
		                               Created_at TIMESTAMP
		                               )""")
		       
	            #query to check if card exists but if the date created is older than 9 weeks then  should not be allowed
	            cur.execute("""SELECT * FROM card_db """)
	            cur.execute("""SELECT * FROM card_db WHERE Card_num = %s AND Created_at < %s""", (self.card_num,nine_weeks_ago))                        
		   	# query to check if the card_num exists and not check expiry
	            expired_card = cur.fetchone()
	            
	            # if the card is older than 5 weeks then dont allow in any enty 
	            if expired_card :
	            	flash("Sorry, this card is expired!")
	            else:
	            	# Check if the card is valid (not expired)
	            	cur.execute("""SELECT * FROM card_db """)
	            	cur.execute("""SELECT * FROM card_db WHERE Card_num = %s AND Card_code = %s""", (self.card_num, self.card_code))
	            	valid_card = cur.fetchone()     	
		            #when card is registered then save in session, continue to view page then save on online_tb
	            	if valid_card: # when a result is found 
		            	session['card_num']=self.card_num
		            	session['card_code']=self.card_code
		            	#after saving on session then add the card_num to online_tb and continue to view page
		            	cur.execute(""" CREATE TABLE if not exists online_tb (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num TEXT,
			                               Created_at TIMESTAMP
			                               )""")
		            	data = [self.card_num, self.created_at]
		            	cur.execute(""" 
			                                	INSERT INTO online_tb(Card_num,Created_at) VALUES(%s,%s)
			            				""", data)
		            	flash("Welcome back to Digital read")
		            	return redirect(url_for("view_bp.View"))
		            #if card is not registered then save it on cards data base and continue to view page
	            	else: 
		            	cur.execute(""" CREATE TABLE if not exists card_db (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num TEXT,
			                               Card_code TEXT, 
			                               Created_at TIMESTAMP
			                               )""")
		            	data = [self.card_num, self.card_code, self.created_at]
		            	#register the card on the card_db
		            	cur.execute(""" 
			                                	INSERT INTO card_db(Card_num, Card_code, created_at) VALUES(%s,%s,%s)
			            				""", data)
			            				
			        #add the card on the online table and save on session
		            	session['card_num']=self.card_num
		            	session['card_code']=self.card_code
		            	#after saving on session then add the card_num to online_tb
		            	cur.execute(""" CREATE TABLE if not exists online_tb (
			                               Id SERIAL PRIMARY KEY,
			                               Card_num TEXT,
			                               Created_at TIMESTAMP
			                               )""")
		            	data = [self.card_num, self.created_at]
		            	cur.execute(""" 
			                                	INSERT INTO online_tb(Card_num, Created_at) VALUES(%s,%s)
			            				""", data) 
			            				
		            	flash("Enjoy your say on Digital read.")
		            	return redirect(url_for("view_bp.View"))
		            	#welcome the user          		
			        #commit and save the changes and save changes
       							         
            conn.commit()  
		            #if there is an error in the database then flash a message
        except Exception as e:
        	flash(f"⚠An Error occured{e}")
        finally:
        	pass

