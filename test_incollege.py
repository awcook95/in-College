import sqlite3
from io import StringIO
import pytest
from collections import namedtuple

import dbfunctions as db
import settings
import states
import users
import utils
import ui

# Notes:
# StringIO simulates a file to hold simulated inputs (inputs separated by \n)
# monkeypatch: needed to simulate user input
# capfd: used to capture text that was output to console


def testtest(capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username", "password", "first", "last")
    db.insertProfilePage(cursor, "username", "major", "uni", "about")
    db.insertProfileJob(cursor, "username", "title", "emp", "2029", "2030", "basement", "gamin")
    db.insertProfileJob(cursor, "username", "title2", "emp2", "2029", "2030", "2nd basement", "moar gamin")
    db.insertProfileEducation(cursor, "username", "USF", "CS", "2018", "2020")
    ui.printProfilePage(cursor, "username")
    out, err = capfd.readouterr()
    assert out == "hello"


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
    db.insertUser(cursor, "username", "password", "first", "last")
    assert db.getUserByName(cursor, "username")  # Check successful insert
    connection.close()


def testCreateSixUsers(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    db.insertUser(cursor, "username2", "password", "first1", "last1")
    db.insertUser(cursor, "username3", "password", "first2", "last2")
    db.insertUser(cursor, "username4", "password", "first3", "last3")
    db.insertUser(cursor, "username5", "password", "first4", "last4")
    users.createUser(cursor, connection)
    out, err = capfd.readouterr()  # Output should display max users created
    assert out == "All permitted accounts have been created, please come back later\n"
    assert db.getNumUsers(cursor) == 5


def testUserAlreadyExists(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("username1\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    users.createUser(cursor, connection)  # todo: fix - Fails because it gets trapped in while loop
    out, err = capfd.readouterr()
    assert out == "Enter your desired username: Sorry, that username has already been taken\n"
    assert settings.currentState == states.loggedOut


def testValidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    db.insertUserSettings(cursor, "username1", "test@gmail.com", "123-123-1234", 0, "English")
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\n"))  # Patch in user input
    users.loginUser(cursor)
    out, err = capfd.readouterr()  # Output should display successfully sign in and state change
    assert out == "Enter your username: Enter your password: You have successfully logged in.\n"
    assert settings.signedIn


def testInvalidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\n"))
    settings.signedIn = False  # fix
    users.loginUser(cursor)  # Fails because it gets trapped in while loop
    out, err = capfd.readouterr()
    assert out == "Enter your username: Enter your password: Incorrect username / password, please try again\n"
    assert not settings.signedIn


def testValidUserLogout():
    settings.signedIn = True
    out = users.logOutUser()
    assert out  # Returns true on successful log out


def testJobSearch(monkeypatch, capfd):
    # Need to update this test when we build the real job search function
    monkeypatch.setattr("sys.stdin", StringIO("A\n"))
    settings.currentState = states.mainMenu  ##
    ui.enterInitialMenu()
    assert settings.currentState == states.mainMenu # Check for still in mainMenu until under construction is replaced


def testValidFriendSearch(monkeypatch):  # todo: fix (broke because of change in findUser function)
    monkeypatch.setattr("sys.stdin", StringIO("5\n"))
    settings.currentState = states.userSearch  ##
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    # out = users.findUser(cursor, "first", "last")  # Returns true if user is found
    # assert out


def testInvalidFriendSearch(monkeypatch):  # todo: fix (broke because of change in findUser function)
    monkeypatch.setattr("sys.stdin", StringIO("2\n"))
    settings.currentState = states.userSearch
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    # out = incollege.findUser(cursor, "notFirst", "last")  # Should return false as user doesn't exist
    # assert not out


def testValidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("D\n"))
    settings.currentState = states.selectSkill
    out = ui.enterSkillMenu()
    assert out


def testInvalidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Z\n"))
    settings.currentState = states.selectSkill
    out = ui.enterSkillMenu()
    assert not out  # Skill menu returns false if exit option is chosen in menu


def testValidJobPost(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Title\nDescription\nEmpName\nLocation\n1"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    settings.signedInUname = "username1"

    users.postJob(cursor)
    out = db.getJobByTitle(cursor, "Title")  # Confirms that job has been added into DB correctly
    assert out is not None

    
def testUsefulLinks(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("e\n"))
    settings.currentState = states.mainMenu
    ui.enterMainMenu()
    assert settings.currentState == states.usefulLinks
    

def testImportantLinks(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("f\n"))
    settings.currentState = states.mainMenu
    ui.enterMainMenu()
    assert settings.currentState == states.importantLinks
    

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
    db.insertUser(cursor, "uname", "password", "first", "last")
    db.insertProfilePage(cursor, "uname", "major", "university", "about")
    for _ in range(3): #add 3 jobs
        db.insertProfileJob(cursor, "uname", "title", "employer", "date_start", "date_end", "location", "job_description")
    settings.currentState = states.profilePage #settings needed for enterProfilePageMenu to work
    settings.signedInUname = "uname"
    monkeypatch.setattr("sys.stdin", StringIO("a\nd\nz\nz\n")) #navigate menu. pressing d tries to add a new job which should fail
    ui.enterProfilePageMenu(cursor)
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
    db.initTables(cursor)
    db.insertUserFriend(cursor, "uname", "friend_uname")
    settings.currentState = states.friendsMenu
    settings.signedInUname = "uname"
    monkeypatch.setattr("sys.stdin", StringIO("Z\n"))
    ui.enterFriendsMenu(cursor)
    out, err = capfd.readouterr()
    assert out is not None
    assert settings.currentState == states.mainMenu
    assert getUserFriendsByName(cursor, "uname") is not None
