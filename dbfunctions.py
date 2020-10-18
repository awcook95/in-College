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

    cursor.execute(""" CREATE TABLE IF NOT EXISTS
    friend_requests(
        sender_uname TEXT,
        reciever_uname TEXT,
        FOREIGN KEY (sender_uname) REFERENCES users(uname)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    profile_page(
        uname TEXT PRIMARY KEY,
        major TEXT,
        university TEXT,
        about TEXT,
        FOREIGN KEY(uname) REFERENCES users(uname)
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    profile_jobs(
        job_id INTEGER PRIMARY KEY,
        uname TEXT,
        title TEXT,
        employer TEXT,
        date_start TEXT,
        date_end TEXT,
        location TEXT,
        job_description TEXT,
        FOREIGN KEY(uname) REFERENCES users(uname)
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    profile_education(
        uni_id INTEGER PRIMARY KEY,
        uname TEXT,
        university_name TEXT,
        user_degree TEXT,
        year_start TEXT,
        year_end TEXT,
        FOREIGN KEY(uname) REFERENCES users(uname)
        )""")


def getProfilePage(cursor, uname):
    cursor.execute("SELECT * FROM profile_page WHERE uname=?", [uname])
    return cursor.fetchone()


def getProfileJobs(cursor, uname):
    cursor.execute("SELECT * FROM profile_jobs WHERE uname=?", [uname])
    return cursor.fetchall()


def getProfileEducation(cursor, uname):
    cursor.execute("SELECT * FROM profile_education WHERE uname=?", [uname])
    return cursor.fetchall()


def insertProfileEducation(cursor, uname, university_name, user_degree, year_start, year_end):
    cursor.execute("INSERT INTO profile_education VALUES (?, ?, ?, ?, ?, ?)", [None, uname, university_name, user_degree, year_start, year_end])


def updateProfileEducation(cursor, uname, university_name, user_degree, year_start, year_end):
    cursor.execute("UPDATE profile_education SET university_name=?, user_degree=?, year_start=?, year_end=? WHERE uname=?", [university_name, user_degree, year_start, year_end, uname])


def insertProfileJob(cursor, uname, title, employer, date_start, date_end, location, job_description):
    cursor.execute("INSERT INTO profile_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [None, uname, title, employer, date_start, date_end, location, job_description])


def updateProfileJob(cursor, uname, title, employer, date_start, date_end, location, job_description):
    cursor.execute("UPDATE profile_jobs SET title=?, employer=?, date_start=?, date_end=?, location=?, job_description=? WHERE uname=?", [title, employer, date_start, date_end, location, job_description, uname])


def insertProfilePage(cursor, uname, major, university, about):
    cursor.execute("INSERT INTO profile_page VALUES (?, ?, ?, ?)", [uname, major, university, about])


def updateProfilePage(cursor, uname, major, university, about):
    cursor.execute("UPDATE profile_page SET major=?, university=?, about=? WHERE uname=?", [major, university, about, uname])


def getUserByFullName(cursor, first, last): # Modified to ignore case
    cursor.execute("SELECT * FROM users WHERE UPPER(firstname)=? AND UPPER(lastname)=? LIMIT 1", [first.upper(), last.upper()])
    return cursor.fetchone()

def getUsersByLastName(cursor, last):
    cursor.execute("SELECT * FROM users WHERE UPPER(lastname)=?", [last.upper()])
    return cursor.fetchall()

def getUsersByParameter(cursor, param_string):
    query = "SELECT * FROM profile_page WHERE " + param_string
    cursor.execute(query)
    return cursor.fetchall()


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
    cursor.execute("SELECT friend_uname FROM user_friends WHERE UPPER(uname)=?", [uname.upper()])
    return cursor.fetchall()

def checkUserFriendRelation(cursor, name, friend):
    cursor.execute("SELECT COUNT(*) FROM user_friends WHERE UPPER(uname)=? AND UPPER(friend_uname)=?", [name.upper(), friend.upper()])
    test = cursor.fetchone()
    return test[0] == 1

def insertUserFriend(cursor, uname, friend_uname):
    cursor.execute("INSERT INTO user_friends VALUES (?, ?, ?)", [None, uname, friend_uname])

def deleteUserFriend(cursor, uname, friend_uname):
    cursor.execute("DELETE FROM user_friends WHERE UPPER(uname)=? AND UPPER(friend_uname)=?", [uname.upper(), friend_uname.upper()])

def insertFriendRequest(cursor, sender_name, reciever_name):
    cursor.execute("INSERT INTO friend_requests VALUES (?, ?)", [sender_name, reciever_name])

def deleteFriendRequest(cursor, sender, reciever):
    cursor.execute("DELETE FROM friend_requests WHERE UPPER(sender_uname)=? AND UPPER(reciever_uname)=? ", [sender.upper(), reciever.upper()])

def getUserFriendRequests(cursor, reciever_name):
    cursor.execute("SELECT * FROM friend_requests WHERE UPPER(reciever_uname)=?", [reciever_name.upper()])
    return cursor.fetchall()
