import sqlite3

dbpath = 'MyTwtr.sqlite3'

connection = sqlite3.connect(dbpath)

cursor = connection.cursor()

def add_user(username, password):
    try:
        cursor.execute("INSERT INTO users(name, passwd) VALUES(?, ?)", (usename, password))
        
connection.close()
