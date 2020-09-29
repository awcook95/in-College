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


def getUserByName(cursor, uname):
    cursor.execute("SELECT * FROM users WHERE uname=?", [uname])
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
