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
    db.insertUser(cursor, "username", "password")
    assert db.getUserByName(cursor, "username")
    connection.close()


def testCreateSixUsers(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password")
    db.insertUser(cursor, "username2", "password")
    db.insertUser(cursor, "username3", "password")
    db.insertUser(cursor, "username4", "password")
    db.insertUser(cursor, "username5", "password")
    incollege.createUser(cursor)
    out, err = capfd.readouterr()
    assert out == "All permitted accounts have been created, please come back later\n"
    assert db.getNumUsers(cursor) == 5


def testUserAlreadyExists(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password")
    monkeypatch.setattr("sys.stdin", StringIO("username1\n"))
    incollege.createUser(cursor)
    out, err = capfd.readouterr()
    assert out == "Enter your desired username: Sorry, that username has already been taken\n"
    assert incollege.state == incollege.loggedOut


def testValidUserLogin(monkeypatch, capfd):
    connection = sqlite3.connect("incollege_test.db")
    cursor = connection.cursor()
    db.initTables(cursor)
    db.insertUser(cursor, "username1", "password")
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
    signedIn = True
    out = incollege.logOutUser(signedIn)
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


def testFriendSearch(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("5\n6\n"))
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


def testSkillSearch(monkeypatch, capfd):
    monkeypatch.setattr("sys.stdin", StringIO("1\n6\n"))
    incollege.state = incollege.selectSkill
    incollege.enterSkillMenu()
    out, err = capfd.readouterr()
    assert out == "What skill would you like to learn?:\n" \
                  "1. Python\n" \
                  "2. How to make a resume\n"\
                  "3. Scrum\n" \
                  "4. Jira\n" \
                  "5. Software Engineering\n" \
                  "6. None - return to menu\n" \
                  "Under Construction\n" \
                  "What skill would you like to learn?:\n" \
                  "1. Python\n" \
                  "2. How to make a resume\n" \
                  "3. Scrum\n" \
                  "4. Jira\n" \
                  "5. Software Engineering\n" \
                  "6. None - return to menu\n"
    assert incollege.state == incollege.loggedOut
