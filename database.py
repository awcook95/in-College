def initTables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS
    users(
        uname TEXT PRIMARY KEY,
        pword TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        plus_member INTEGER,
        date_created TEXT,
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

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    user_job_applications(
        app_id INTEGER PRIMARY KEY,
        applicant_uname TEXT,
        job_title TEXT,
        graduation_date TEXT,
        start_date TEXT, 
        credentials TEXT,
        applied_date TEXT,
        FOREIGN KEY(job_title) REFERENCES jobs(title)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    favorited_jobs(
        uname TEXT,
        job_title TEXT,
        FOREIGN KEY(uname) REFERENCES jobs(uname)
        FOREIGN KEY(job_title) REFERENCES jobs(title)
        PRIMARY KEY(uname, job_title)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    messages(
        message_id INTEGER PRIMARY KEY,
        sender_uname TEXT,
        receiver_uname TEXT,
        body TEXT,
        read INTEGER,
        FOREIGN KEY(sender_uname) REFERENCES users(uname)
        FOREIGN KEY(receiver_uname) REFERENCES users(uname)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    notifications(
        notification_id INTEGER PRIMARY KEY,
        type TEXT,
        body TEXT,
        receiver_uname TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    user_completed_trainings(
        training_id INTEGER PRIMARY KEY,
        uname TEXT,
        training_name TEXT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    trainings(
        training_id INTEGER PRIMARY KEY,
        training_name TEXT,
        FOREIGN KEY(training_name) REFERENCES user_completed_trainings(training_name)
    )""")

# ========================================= USERS =========================================

def insertUser(cursor, uname, pword, fname, lname, plusMember, date_created):
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", [uname, pword, fname, lname, plusMember, date_created])  # plusMember is boolean


def getAllOtherUsers(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname !=?", [uname])
    return cursor.fetchall()


def getUserFullName(cursor, uname):
    cursor.execute("SELECT firstname, lastname FROM Users WHERE UPPER(uname)=?", [uname.upper()])
    user = cursor.fetchone()
    return user[0] + " " + user[1]


def getUserByFullName(cursor, first, last):
    cursor.execute("SELECT * FROM users WHERE UPPER(firstname)=? AND UPPER(lastname)=? LIMIT 1", [first.upper(), last.upper()])
    return cursor.fetchone()


def getUsersByLastName(cursor, last):
    cursor.execute("SELECT * FROM users WHERE UPPER(lastname)=?", [last.upper()])
    return cursor.fetchall()


def getUsersByParameter(cursor, param_string):
    query = "SELECT * FROM profile_page WHERE " + param_string
    cursor.execute(query)
    return cursor.fetchall()


def getUserCreatedDate(cursor, uname):
    cursor.execute("SELECT date_created FROM users WHERE UPPER(uname)=?", [uname.upper()])
    d = cursor.fetchone()
    return d[0]


def getUserByName(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname=?", [uname])
    return cursor.fetchone()


def getNumUsers(cursor):
    cursor.execute("SELECT COUNT(uname) FROM users")
    return cursor.fetchone()[0]


def tryLogin(cursor, uname, pword):
    cursor.execute("SELECT * FROM users WHERE uname=? AND pword=?", [uname, pword])
    return cursor.fetchone()


def userIsPlusMember(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname=?", [uname])
    user = cursor.fetchone()
    return user[4] == 1


def getAllUsers(cursor):
    cursor.execute("Select * from users")
    return cursor.fetchall()


# ========================================= SETTINGS =========================================

def insertUserSettings(cursor, uname, email, sms, advert, language):
    cursor.execute("INSERT INTO user_settings VALUES (?, ?, ?, ?, ?)", [uname, email, sms, advert, language])


def updateUserSettings(cursor, uname, email, sms, advert):
    cursor.execute("UPDATE user_settings SET emailnotif=?, smsnotif=?, targetadvert=? WHERE uname=?", [email, sms, advert, uname])


def updateUserLanguage(cursor, uname, language):
    cursor.execute("UPDATE user_settings SET languagepref=? WHERE uname=?", [language, uname])


def getUserSettingsByName(cursor, uname):
    cursor.execute("SELECT * FROM user_settings WHERE uname=?", [uname])
    return cursor.fetchone()


# ========================================= PROFILES =========================================

def insertProfilePage(cursor, uname, major, university, about):
    cursor.execute("INSERT INTO profile_page VALUES (?, ?, ?, ?)", [uname, major, university, about])


def insertProfileEducation(cursor, uname, university_name, user_degree, year_start, year_end):
    cursor.execute("INSERT INTO profile_education VALUES (?, ?, ?, ?, ?, ?)", [None, uname, university_name, user_degree, year_start, year_end])


def insertProfileJob(cursor, uname, title, employer, date_start, date_end, location, job_description):
    cursor.execute("INSERT INTO profile_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [None, uname, title, employer, date_start, date_end, location, job_description])


def updateProfilePage(cursor, uname, major, university, about):
    cursor.execute("UPDATE profile_page SET major=?, university=?, about=? WHERE uname=?", [major, university, about, uname])


def updateProfileEducation(cursor, uname, university_name, user_degree, year_start, year_end):
    cursor.execute("UPDATE profile_education SET university_name=?, user_degree=?, year_start=?, year_end=? WHERE uname=?", [university_name, user_degree, year_start, year_end, uname])


def updateProfileJob(cursor, uname, title, employer, date_start, date_end, location, job_description):
    cursor.execute("UPDATE profile_jobs SET title=?, employer=?, date_start=?, date_end=?, location=?, job_description=? WHERE uname=?", [title, employer, date_start, date_end, location, job_description, uname])


def getProfilePage(cursor, uname):
    cursor.execute("SELECT * FROM profile_page WHERE uname=?", [uname])
    return cursor.fetchone()


def getProfileJobs(cursor, uname):
    cursor.execute("SELECT * FROM profile_jobs WHERE uname=?", [uname])
    return cursor.fetchall()


def getProfileEducation(cursor, uname):
    cursor.execute("SELECT * FROM profile_education WHERE uname=?", [uname])
    return cursor.fetchall()


def profilePageExists(cursor, uname):
    profile = getProfilePage(cursor, uname)
    # MODIFIED EPIC 10
    return not (profile[1] == "" and profile[2] == "" and profile[3] == "")


# ========================================= FRIENDS =========================================

def insertUserFriend(cursor, uname, friend_uname):
    cursor.execute("INSERT INTO user_friends VALUES (?, ?, ?)", [None, uname, friend_uname])


def insertFriendRequest(cursor, sender_name, receiver_name):
    cursor.execute("INSERT INTO friend_requests VALUES (?, ?)", [sender_name, receiver_name])


def deleteUserFriend(cursor, uname, friend_uname):
    cursor.execute("DELETE FROM user_friends WHERE UPPER(uname)=? AND UPPER(friend_uname)=?", [uname.upper(), friend_uname.upper()])


def deleteFriendRequest(cursor, sender, receiver):
    cursor.execute("DELETE FROM friend_requests WHERE UPPER(sender_uname)=? AND UPPER(reciever_uname)=? ", [sender.upper(), receiver.upper()])


def getUserFriends(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname IN (SELECT friend_uname FROM user_friends WHERE uname=?)", [uname])
    return cursor.fetchall()


def getUserFriendsByName(cursor, uname):
    cursor.execute("SELECT friend_uname FROM user_friends WHERE UPPER(uname)=?", [uname.upper()])
    return cursor.fetchall()


def getUserFriendRequests(cursor, receiver_name):
    cursor.execute("SELECT * FROM friend_requests WHERE UPPER(reciever_uname)=?", [receiver_name.upper()])
    return cursor.fetchall()


def checkUserFriendRelation(cursor, name, friend):
    cursor.execute("SELECT COUNT(*) FROM user_friends WHERE UPPER(uname)=? AND UPPER(friend_uname)=?", [name.upper(), friend.upper()])
    test = cursor.fetchone()
    return test[0] == 1


# ========================================= MESSAGES =========================================

def insertMessage(cursor, senderUname, receiverUname, body):
    cursor.execute("INSERT INTO messages VALUES(?,?,?,?,?)", [None, senderUname, receiverUname, body, 0])  # last element is boolean read/unread


def deleteMessage(cursor, messageID):
    cursor.execute("DELETE FROM messages WHERE message_id=?", [messageID])


def updateMessageAsRead(cursor, messageID):
    cursor.execute("UPDATE messages SET read=1 WHERE message_id=?", [messageID])


def getMessageByReceiver(cursor, receiverUname):
    cursor.execute("SELECT * FROM messages WHERE receiver_uname=?", [receiverUname])
    return cursor.fetchall()


def hasUnreadMessages(cursor, uname):
    cursor.execute("SELECT read FROM messages WHERE receiver_uname=? AND read = 0", [uname])
    unreadMessages = cursor.fetchall()
    return len(unreadMessages) > 0


# ========================================= JOBS =========================================

def insertJob(cursor, title, desc, emp, loc, sal, author):
    cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)", [None, title, desc, emp, loc, sal, author])


def insertUserJobApplication(cursor, applicant_uname, job_title, graduation_date, start_date, credentials, applied_date):
    cursor.execute("INSERT INTO user_job_applications VALUES(?,?,?,?,?,?,?)", [None, applicant_uname, job_title, graduation_date, start_date, credentials, applied_date])


def insertFavoriteJob(cursor, uname, job_title):
    cursor.execute("INSERT INTO favorited_jobs VALUES(?,?)", [uname, job_title])


def deleteJob(cursor, jobID):
    cursor.execute("DELETE FROM jobs WHERE jobID=?", [jobID])


def deleteFavoriteJob(cursor, uname, jobTitle):
    cursor.execute("DELETE FROM favorited_jobs WHERE UPPER(uname)=? AND job_title=?", [uname.upper(), jobTitle])


def getAllJobs(cursor):
    cursor.execute("SELECT * FROM jobs")
    return cursor.fetchall()


def getJobsByAuthor(cursor, author):
    cursor.execute("SELECT * FROM jobs WHERE author=?", [author])
    return cursor.fetchall()


def getJobByTitle(cursor, title):
    cursor.execute("SELECT * FROM jobs WHERE Title like ?", [title])
    return cursor.fetchone()


def getNumJobs(cursor):
    cursor.execute("SELECT COUNT(jobID) FROM jobs")
    return cursor.fetchone()[0]


def getUserJobApplicationByTitle(cursor, applicant_name, job_title):
    cursor.execute("SELECT * FROM user_job_applications WHERE UPPER(applicant_uname)=? AND job_title=?", [applicant_name.upper(), job_title])
    return cursor.fetchall()


def getUnappliedJobs(cursor, uname):
    cursor.execute("SELECT * FROM jobs WHERE title NOT IN (SELECT job_title FROM user_job_applications WHERE applicant_uname=?)", [uname])
    return cursor.fetchall()


def getAppliedJobs(cursor, uname):
    cursor.execute("SELECT * FROM jobs WHERE title IN (SELECT job_title FROM user_job_applications WHERE applicant_uname=?)", [uname])
    return cursor.fetchall()


def getJobsPostedByUser(cursor, authorName):
    cursor.execute("SELECT * FROM jobs WHERE UPPER(author)=?", [authorName.upper()])
    return cursor.fetchall()


def getJobAppliedDate(cursor, uname):
    cursor.execute("SELECT applied_date FROM user_job_applications WHERE UPPER(applicant_uname)=? ORDER BY applied_date DESC", [uname.upper()])
    d = cursor.fetchone()
    return None if d is None else d[0]


def getFavoriteJobsByUser(cursor, uname):
    cursor.execute("SELECT * FROM jobs WHERE title IN (SELECT job_title FROM favorited_jobs WHERE uname=?)", [uname])
    return cursor.fetchall()


def getJobsNotFavorited(cursor, uname):
    cursor.execute("SELECT * FROM jobs WHERE title NOT IN (SELECT job_title FROM favorited_jobs WHERE uname=?)", [uname])
    return cursor.fetchall()


def getJobApplicantsByTitle(cursor, job_title):
    cursor.execute("SELECT applicant_uname FROM user_job_applications WHERE job_title=?", [job_title])
    return cursor.fetchall()

# Used for applied jobs API to pull back username and why they are right for job
def getJobApplicationDetailsByTitle(cursor, job_title):
    cursor.execute("SELECT applicant_uname, credentials from user_job_applications WHERE job_title=?", [job_title])


# ========================================= NOTIFICATIONS =========================================

def insertNotification(cursor, notification_type, body, receiver):
    cursor.execute("INSERT INTO notifications VALUES(?,?,?,?)", [None, notification_type, body, receiver])


def deleteNotification(cursor, notification_type, body, receiver):
    cursor.execute("DELETE FROM notifications WHERE type=? AND body=? AND receiver_uname=?",
                   [notification_type, body, receiver])


def getNotificationsForUserByType(cursor, notification_type, receiver):
    cursor.execute("SELECT * FROM notifications WHERE type=? AND receiver_uname=?", [notification_type, receiver])
    return cursor.fetchall()


# ========================================= TRAININGS =========================================

def insertUserCompletedTraining(cursor, uname, training_name):
    cursor.execute("INSERT INTO user_completed_train VALUES(?,?,?)", [None, uname, training_name])


def getUserCompletedTrianingByTitle(cursor, uname, training_name):
    cursor.execute("SELECT * FROM user_completed_trainings WHERE uname=? AND training_name=?", [uname, training_name])
    return cursor.fetchall()

def insertNewTraining(cursor, training_name):
    cursor.execute("INSERT INTO trainings VALUES(?, ?)", [None, training_name])
    return cursor.fetchall()

def getAllTrainings(cursor):
    cursor.execute("SELECT * FROM trainings")
    return cursor.fetchall()
