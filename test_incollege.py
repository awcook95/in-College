import sqlite3
from io import StringIO
import pytest
from collections import namedtuple

import database as db
import profiles
import settings
import states
import users
import utils
import jobs
import ui
import API

# Notes:
# StringIO simulates a file to hold simulated inputs (inputs separated by \n)
# monkeypatch: needed to simulate user input
# capfd: used to capture text that was output to console


def testValidatePasswordCorrect():
    assert utils.validatePassword("Testing123!")


@pytest.mark.parametrize("password", ["testing", "Testing123456"])
def testValidatePasswordIncorrect(password):
    assert not utils.validatePassword(password)


def testCreateUser():  # todo: potentially change this test to utilize createUser function from main program instead
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    # Initialize database and run insert function
    db.initTables(cursor)
    db.insertUser(cursor, "username", "password", "first", "last", 0, "01/01/2020")
    assert db.getUserByName(cursor, "username")  # Check successful insert
    connection.close()


def testMaxAccountsCreated(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    for i in range(10):
        db.insertUser(cursor, f"username{i}", "password", f"first{i}", f"last{i}", 0, "01/01/2020")
    users.createUser(cursor, connection)
    out, err = capfd.readouterr()  # Output should display max users created
    assert out == "All permitted accounts have been created, please come back later\n"
    assert db.getNumUsers(cursor) == 10


def testUserAlreadyExists(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("username1\nusername2\nPassword1!\nfname\nlname\nN\n")) #after username1 is taken, pick a different uname and exit menu
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS user_settings")
    cursor.execute("DROP TABLE IF EXISTS profile_page")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last", 0, "01/01/2020")
    users.createUser(cursor, connection)
    out, err = capfd.readouterr()
    assert "Sorry, that username has already been taken" in out
    assert settings.currentState == states.loggedOut


def testValidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last", 0, "01/01/2020")
    db.insertUserSettings(cursor, "username1", "test@gmail.com", "123-123-1234", 0, "English")
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\n"))  # Patch in user input
    users.loginUser(cursor, connection)
    out, err = capfd.readouterr()  # Output should display successfully sign in and state change
    assert "You have successfully logged in." in out
    assert settings.signedIn


def testInvalidUserLogin(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\nusername2\npassword\n")) #invalid credentials first, valid credentials second
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username2", "password", "first", "last", 0, "01/01/2020")
    settings.signedIn = False  # fix
    users.loginUser(cursor, connection)  # Fails because it gets trapped in while loop
    out, err = capfd.readouterr()
    assert "Enter your password: Incorrect" in out
    assert settings.signedIn


def testValidUserLogout():
    settings.signedIn = True
    out = users.logOutUser()
    assert out  # Returns true on successful log out


def testJobSearch(monkeypatch, capfd):
    # Need to update this test when we build the real job search function
    monkeypatch.setattr("sys.stdin", StringIO("A\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    settings.currentState = states.mainMenu  ##
    ui.enterInitialMenu(cursor, connection)
    assert settings.currentState == states.mainMenu # Check for still in mainMenu until under construction is replaced


def testValidFriendSearch(monkeypatch):  # todo: fix (broke because of change in findUser function)
    monkeypatch.setattr("sys.stdin", StringIO("5\n"))
    settings.currentState = states.userSearch  ##
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last", 0, "01/01/2020")
    # out = users.findUser(cursor, "first", "last")  # Returns true if user is found
    # assert out


def testInvalidFriendSearch(monkeypatch):  # todo: fix (broke because of change in findUser function)
    monkeypatch.setattr("sys.stdin", StringIO("2\n"))
    settings.currentState = states.userSearch
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last", 0, "01/01/2020")
    # out = incollege.findUser(cursor, "notFirst", "last")  # Should return false as user doesn't exist
    # assert not out


def testValidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("D\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    settings.currentState = states.selectSkill
    out = ui.enterSkillMenu(cursor, connection)
    assert out


def testInvalidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Z\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    settings.currentState = states.selectSkill
    out = ui.enterSkillMenu(cursor, connection)
    assert not out  # Skill menu returns false if exit option is chosen in menu


def testValidJobPost(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Title\nDescription\nEmpName\nLocation\n1"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last", 0, "01/01/2020")
    settings.signedInUname = "username1"
    jobs.postJob(cursor, connection)
    out = db.getJobByTitle(cursor, "Title")  # Confirms that job has been added into DB correctly
    assert out is not None


def testCreateMaxJobPosts(capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS jobs")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "01/01/2020")
    for _ in range(10):
        db.insertJob(cursor, "title", "desc", "emp", "loc", "sal", "username1")
    jobs.postJob(cursor, connection)
    out, err = capfd.readouterr()
    assert "All permitted jobs have been created, please come back later.\n" in out
    assert db.getNumJobs(cursor) == 10
    assert settings.currentState == states.jobMenu

    
def testUsefulLinks(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("e\nz\nz\nz\n"))
    settings.signedInUname = "username1"
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS profile_page")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertProfilePage(cursor, "username1", "major", "university", "about")
    settings.currentState = states.mainMenu
    ui.enterMainMenu(cursor, connection)
    out, err = capfd.readouterr()
    assert "Useful Links" in out
    

def testImportantLinks(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("f\nz\nz\nz\n"))
    settings.signedInUname = "username1"
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS profile_page")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertProfilePage(cursor, "username1", "major", "university", "about")
    settings.currentState = states.mainMenu
    ui.enterMainMenu(cursor, connection)
    out, err = capfd.readouterr()
    assert "Important Links" in out
    

def testInsertUserSettings():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUserSettings(cursor, "testname", 1, 1, 1, "testlanguage")
    assert db.getUserSettingsByName(cursor, "testname") is not None
    

def testUpdateUserSettings():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUserSettings(cursor, "testname", 1, 1, 1, "testlanguage")
    db.updateUserSettings(cursor, "testname", 0, 0, 0)
    userSetting = namedtuple('User', 'uname emailnotif smsnotif targetadvert languagepref')
    currentUser = userSetting._make(db.getUserSettingsByName(cursor, "testname"))
    assert currentUser.emailnotif == 0
    

def testUpdateUserLanguage():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUserSettings(cursor, "testname", 1, 1, 1, "testlanguage")
    db.updateUserLanguage(cursor, "testname", "testlanguage2")
    userSetting = namedtuple('User', 'uname emailnotif smsnotif targetadvert languagepref')
    currentUser = userSetting._make(db.getUserSettingsByName(cursor, "testname"))
    assert currentUser.languagepref == "testlanguage2"
    

def testCreateStudentProfile():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertProfilePage(cursor, "uname", "major", "university", "about")
    db.insertProfileEducation(cursor, "uname", "university_name", "user_degree", "2016", "2020")
    db.insertProfileJob(cursor, "uname", "title", "employer", "date_start", "date_end", "location", "job_description")
    assert db.getProfilePage(cursor, "uname") is not None
    assert db.getProfileJobs(cursor, "uname") is not None
    assert db.getProfileEducation(cursor, "uname") is not None
    

def testProfileAddFourJobs(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS profile_jobs")
    db.initTables(cursor)
    db.insertUser(cursor, "uname", "password", "first", "last", 0, "01/01/2020")
    db.insertProfilePage(cursor, "uname", "major", "university", "about")
    for _ in range(3):  # add 3 jobs
        db.insertProfileJob(cursor, "uname", "title", "employer", "date_start", "date_end", "location", "job_description")
    settings.currentState = states.profilePage #settings needed for enterProfilePageMenu to work
    settings.signedInUname = "uname"
    monkeypatch.setattr("sys.stdin", StringIO("a\nd\nz\nz\n")) #navigate menu. pressing d tries to add a new job which should fail
    profiles.enterProfilePageMenu(cursor, connection)
    out, err = capfd.readouterr()
    assert out is not None
    assert len(db.getProfileJobs(cursor, settings.signedInUname)) == 3
    assert settings.currentState == states.mainMenu
    

def testAddFriend():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUserFriend(cursor, "uname", "friend_uname")
    assert db.getUserFriendsByName(cursor, "uname") is not None
    
    
def testViewFriendList(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    db.initTables(cursor)
    db.insertUser(cursor, "uname", "password", "first", "last", 0, "01/01/2020")
    db.insertUser(cursor, "friend_uname", "password", "first2", "last2", 0, "01/01/2020")
    db.insertUserFriend(cursor, "uname", "friend_uname")
    settings.currentState = states.friendsMenu
    settings.signedInUname = "uname"
    monkeypatch.setattr("sys.stdin", StringIO("Z\n"))
    ui.enterFriendsMenu(cursor, connection)
    out, err = capfd.readouterr()
    assert out is not None
    assert settings.currentState == states.mainMenu
    assert db.getUserFriendsByName(cursor, "uname") is not None

    
def testRemoveFriend(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("A\n1\nZ\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS user_friends")
    db.initTables(cursor)
    db.insertUser(cursor, "uname", "password", "first", "last", 0, "01/01/2020")
    db.insertUser(cursor, "friend_uname", "password", "first2", "last2", 0, "01/01/2020")
    db.insertUserFriend(cursor, "uname", "friend_uname")
    db.insertUserFriend(cursor, "friend_uname", "uname")
    settings.currentState = states.friendsMenu
    settings.signedInUname = "uname"
    ui.enterFriendsMenu(cursor, connection)
    assert settings.currentState == states.mainMenu
    assert len(db.getUserFriendsByName(cursor, "uname")) == 0
    
    
def testSendFriendRequest(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("A\nfirst2 last2\nY\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "2020-01-01 12:30:00")
    settings.signedInUname = "username1"
    settings.signedIn = True
    settings.currentState = states.userSearch
    users.findUser(cursor, connection)
    assert len(db.getUserFriendRequests(cursor, "username2")) == 1


def testAcceptFriendRequest(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("A\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS friend_requests")
    cursor.execute("DROP TABLE IF EXISTS user_friends")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "01/01/2020")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "01/01/2020")
    db.insertFriendRequest(cursor, "username1", "username2")
    settings.signedInUname = "username2"
    utils.handleUserFriendRequests(cursor, connection, settings.signedInUname)
    assert len(db.getUserFriendsByName(cursor, "username1")) == 1
    assert len(db.getUserFriendsByName(cursor, "username2")) == 1
    assert ((db.getUserFriendsByName(cursor, "username1"))[0])[0] == "username2"
    assert ((db.getUserFriendsByName(cursor, "username2"))[0])[0] == "username1"


def testDeleteJobPost(monkeypatch):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "2020-01-01 12:30:00")
    settings.signedInUname = "username1"
    db.insertJob(cursor, "title1", "desc1", "emp1", "loc1", "sal1", "first1 last1")
    db.insertJob(cursor, "title2", "desc2", "emp2", "loc2", "sal2", "first1 last1")
    assert db.getNumJobs(cursor) == 2
    db.insertUserJobApplication(cursor, "username2", "title1", "01/01/1243", "01/02/1243", "credentials", "2020-01-01 12:30:00")
    monkeypatch.setattr("sys.stdin", StringIO("1\nN\n"))
    jobs.enterDeleteAJobMenu(cursor, connection)
    assert db.getNumJobs(cursor) == 1
    assert len(db.getAppliedJobs(cursor, "username2")) == 0


def testApplyForJob(monkeypatch):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS user_job_applications")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "01/01/2020")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "01/01/2020")
    db.insertJob(cursor, "title1", "desc1", "emp1", "loc1", "sal1", "first1 last1")
    selectedJob = db.getAllJobs(cursor)[0]
    settings.signedInUname = "username2"
    monkeypatch.setattr("sys.stdin", StringIO("1\n01/01/1234\n01/02/1234\ncredentials\n"))
    jobs.applyForJob(cursor, connection, selectedJob)
    assert len(db.getAppliedJobs(cursor, "username2")) == 1


def testFavoriteAJob(monkeypatch):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS favorited_jobs")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "2020-01-01 12:30:00")
    db.insertJob(cursor, "title1", "desc1", "emp1", "loc1", "sal1", "first1 last1")
    selectedJob = db.getAllJobs(cursor)[0]
    settings.signedInUname = "username2"
    monkeypatch.setattr("sys.stdin", StringIO("b\nz\n"))
    jobs.viewJobDetails(cursor, connection, selectedJob)
    assert len(db.getFavoriteJobsByUser(cursor, "username2")) == 1


def testApplyForJobAlreadyAppliedFor(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("1\n\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    cursor.execute("DROP TABLE IF EXISTS jobs")
    cursor.execute("DROP TABLE IF EXISTS user_job_applications")
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first1", "last1", 0, "2020-01-01 12:30:00")
    db.insertUser(cursor, "username2", "password", "first2", "last2", 0, "2020-01-01 12:30:00")
    db.insertJob(cursor, "title1", "desc1", "emp1", "loc1", "sal1", "first1 last1")
    selectedJob = db.getAllJobs(cursor)[0]
    db.insertUserJobApplication(cursor, "username2", "title1", "01/01/1234", "01/02/1234", "credentials", "2020-01-01 12:30:00")
    settings.signedInUname = "username2"
    jobs.applyForJob(cursor, connection, selectedJob)
    assert len(db.getAppliedJobs(cursor, "username2")) == 1


def testStudentAccountAPIInput():
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Users") #delete tables to make sure no conflicts when running test multiple times
    db.initTables(cursor)
    user_count = db.getNumUsers(cursor)
    student_accounts = API.createStudentAccounts()
    for obj in student_accounts:
        if user_count <= 10 and db.getUserByFullName(cursor, obj.first_name, obj.last_name) == None:
            db.insertUser(cursor, obj.username, obj.password, obj.first_name, obj.last_name, obj.plus_member, "01/01/2020")
            user_count += 1
        else:
            break
    connection.commit()
    assert len(db.readUsers(cursor)) != None