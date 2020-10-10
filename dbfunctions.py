def initTables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS
    users(
        uname TEXT PRIMARY KEY,
        pword TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        UNIQUE(firstname, lastname)
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    jobs(
        jobID INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        employer TEXT,
        location TEXT,
        salary INTEGER,
        author TEXT,
        FOREIGN KEY(author) REFERENCES users(uname)
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    user_settings(
        uname TEXT PRIMARY KEY,
        emailnotif INTEGER,
        smsnotif INTEGER,
        targetadvert INTEGER,
        languagepref TEXT,
        FOREIGN KEY(uname) REFERENCES users(uname)
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    user_friends(
        friend_id INTEGER PRIMARY KEY,
        uname TEXT,
        friend_uname TEXT,
        FOREIGN KEY(uname) REFERENCES users(uname)
        )""")


def getUserByFullName(cursor, first, last):
    cursor.execute("SELECT * FROM users WHERE firstname=? AND lastname=? LIMIT 1", [first, last])
    return cursor.fetchone()


def insertJob(cursor, title, desc, emp, loc, sal, author):
    cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)", [None, title, desc, emp, loc, sal, author])


def getAllJobs(cursor):
    cursor.execute("SELECT * FROM jobs")
    return cursor.fetchall()


def getJobByTitle(cursor, title):
    cursor.execute("SELECT * FROM jobs WHERE Title like ?", [title])
    return cursor.fetchone()
    

def insertUser(cursor, uname, pword, fname, lname):
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", [uname, pword, fname, lname])


def insertUserSettings(cursor, uname, email, sms, advert, language):
    cursor.execute("INSERT INTO user_settings VALUES (?, ?, ?, ?, ?)", [uname, email, sms, advert, language])


def updateUserSettings(cursor, uname, email, sms, advert):
    cursor.execute("UPDATE user_settings SET emailnotif=?, smsnotif=?, targetadvert=? WHERE uname=?", [email, sms, advert, uname])


def updateUserLanguage(cursor, uname, language):
    cursor.execute("UPDATE user_settings SET languagepref=? WHERE uname=?", [language, uname])


def getUserByName(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname=?", [uname])
    return cursor.fetchone()


def getUserSettingsByName(cursor, uname):
    cursor.execute("SELECT * FROM user_settings WHERE uname=?", [uname])
    return cursor.fetchone()


def getNumUsers(cursor):
    cursor.execute("SELECT COUNT(uname) FROM users")
    #fetchone returns a list like fetchall, so get the first element
    return cursor.fetchone()[0]


def getNumJobs(cursor):
    cursor.execute("SELECT COUNT(jobID) FROM jobs")
    return cursor.fetchone()[0]


def tryLogin(cursor, uname, pword):
    cursor.execute("SELECT * FROM users WHERE uname=? AND pword=?", [uname, pword])
    return cursor.fetchone()


def readUsers(cursor):
    cursor.execute("Select * from users")
    return cursor.fetchall()


def getUserFriendsByName(cursor, uname):
    cursor.execute("SELECT friend_uname FROM user_friends WHERE uname=?", [uname])
    return cursor.fetchall()


def insertUserFriend(cursor, uname, friend_uname):
    cursor.execute("INSERT INTO user_friends VALUES (?, ?, ?)", [None, uname, friend_uname])
