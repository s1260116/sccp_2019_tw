import sqlite3
import hashlib
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')

dbpath = 'MyTwtr.db'

connection = sqlite3.connect(dbpath, check_same_thread=False)

cursor = connection.cursor()

def add_user(username, password):
    encrypted_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        cursor.execute("INSERT INTO users(name, passwd) VALUES(?, ?)", (username, encrypted_pass))
        connection.commit()
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

def login_user(username):
    try:
        cursor.execute("SELECT * FROM users WHERE name=?", (username,))
        userData = cursor.fetchone()
        return userData
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

def post_tweet(user_id, body):
    timeStamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO tweets(user_id, body, tw_time) VALUES(?, ?, ?)", (user_id, body, timeStamp))
        connection.commit()
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])

def get_tweets():
    try:
        cursor.execute("SELECT * FROM tweets ORDER BY tw_time DESC")
        tweetsData = cursor.fetchall()
        return tweetsData
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
