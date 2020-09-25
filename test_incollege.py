import sqlite3
from io import StringIO
import pytest

import dbfunctions as db
import incollege

# Notes:
# StringIO simulates a file to hold simulated inputs (inputs separated by \n)
# monkeypatch: needed to simulate user input
# capfd: used to capture text that was output to console


def testValidatePasswordCorrect():
    assert incollege.validatePassword("Testing123!")


@pytest.mark.parametrize("password", ["testing", "Testing123456"])
def testValidatePasswordIncorrect(password):
    assert not incollege.validatePassword(password)


def testCreateUser():  # todo: potentially change this test to utilize createUser function from main program instead
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username", "password", "first", "last")
    assert db.getUserByName(cursor, "username")
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
    incollege.createUser(cursor)
    out, err = capfd.readouterr()
    assert out == "All permitted accounts have been created, please come back later\n"
    assert db.getNumUsers(cursor) == 5


def testUserAlreadyExists(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("username1\n"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    incollege.createUser(cursor)
    out, err = capfd.readouterr()
    assert out == "Enter your desired username: Sorry, that username has already been taken\n"
    assert incollege.state == incollege.loggedOut


def testValidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\n"))
    incollege.loginUser(cursor)
    out, err = capfd.readouterr()
    assert out == "Enter your username: Enter your password: You have successfully logged in.\n"
    assert incollege.signedIn


def testInvalidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    monkeypatch.setattr("sys.stdin", StringIO("username1\npassword\n"))
    incollege.signedIn = False  # fix
    incollege.loginUser(cursor)
    out, err = capfd.readouterr()
    assert out == "Enter your username: Enter your password: Incorrect username / password, please try again\n"
    assert not incollege.signedIn


def testValidUserLogout():
    incollege.signedIn = True
    out = incollege.logOutUser()
    assert out



def testJobSearch(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("3\n6\n"))
    incollege.state = incollege.loggedOut  # fix
    incollege.enterInitialMenu()
    out, err = capfd.readouterr()
    assert out == "Select Option:\n" \
                  "1. Log in with existing account\n" \
                  "2. Create new account\n" \
                  "3. Search for a job\n" \
                  "4. Learn a new skill\n" \
                  "5. Find someone you know\n" \
                  "6. Quit\n" \
                  "Under Construction\n" \
                  "Select Option:\n" \
                  "1. Log in with existing account\n" \
                  "2. Create new account\n" \
                  "3. Search for a job\n" \
                  "4. Learn a new skill\n" \
                  "5. Find someone you know\n" \
                  "6. Quit\n"


def testValidFriendSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("5\n"))
    incollege.state = incollege.findUser
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    out = incollege.findUser(cursor, "first", "last")
    assert out

def testInvalidFriendSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("2\n"))
    incollege.state = incollege.findUser
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    out = incollege.findUser(cursor, "notFirst", "last")
    assert not out

def testValidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("1\n"))
    incollege.state = incollege.selectSkill
    out = incollege.enterSkillMenu()
    assert out

def testInvalidSkillSearch(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("6\n"))
    incollege.state = incollege.selectSkill
    out = incollege.enterSkillMenu()
    assert not out

def testValidJobPost(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("Title\nDescription\nEmpName\nLocation\n1"))
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password", "first", "last")
    incollege.signedInUname = "username1"
    
    incollege.postJob(cursor)
    out = db.getJobByTitle(cursor, "Title")
    assert out != None
