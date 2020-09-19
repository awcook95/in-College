import sqlite3

def initTables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS
    users(uname TEXT PRIMARY KEY, pword TEXT)""")

def insertUser(cursor, uname, pword):
    cursor.execute("INSERT INTO users VALUES (?, ?)", [uname, pword])

def getUserByName(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname=?", [uname])
    return cursor.fetchone()

def getNumUsers(cursor):
    cursor.execute("SELECT COUNT(uname) FROM users")
    #fetchone returns a list like fetchall, so get the first element
    return cursor.fetchone()[0]

def tryLogin(cursor, uname, pword):
    cursor.execute("SELECT * FROM users WHERE uname=? AND pword=?", [uname, pword])
    return cursor.fetchone()

def readUsers(cursor):
    cursor.execute("Select * from users")
    return cursor.fetchall()