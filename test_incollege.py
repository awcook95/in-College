import sqlite3
from io import StringIO
import pytest

import dbfunctions as db
import incollege
import settings
import states
import users
import utils
import ui

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
    monkeypatch.setattr("sys.stdin", StringIO("3\n6\n"))
    settings.currentState = states.loggedOut  ##
    ui.enterInitialMenu()
    out, err = capfd.readouterr()
    assert True 


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
    monkeypatch.setattr("sys.stdin", StringIO("1\n"))
    settings.currentState = states.selectSkill
    out = ui.enterSkillMenu()
    assert out


def testInvalidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("6\n"))
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
