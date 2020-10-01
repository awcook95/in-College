from collections import namedtuple

import dbfunctions as db
import settings
import states
import utils


def createUser(dbCursor, connection):
    # todo: possibly add exit option in case user wants to cancel account creation

    if db.getNumUsers(dbCursor) >= 5:  # checks if number of accounts in database is at max limit
        print("All permitted accounts have been created, please come back later")
        settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
        return

    uname = input("Enter your desired username: ")
    # added below if statement to return back to main menu if username is taken
    while db.getUserByName(dbCursor, uname):
        print("Sorry, that username has already been taken\n")
        uname = input("Enter your desired username: ")

    pword = input("Enter your desired password: ")
    while not utils.validatePassword(pword):
        print("Invalid password. Must be length 8-12 characters, contain one digit, one uppercase character, and one non-alphanumeric")
        pword = input("Enter your desired password: ")

    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")

    db.insertUser(dbCursor, uname, pword, fname, lname)
    print("Account has been created")
    settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
    connection.commit()  # commits the new account to the database (ensures account is saved)


def loginUser(dbCursor):
    # todo: possibly add exit option in case user wants to cancel account login

    uname = input("Enter your username: ")
    pword = input("Enter your password: ")

    while not db.tryLogin(dbCursor, uname, pword):
        print("Incorrect username / password, please try again\n")
        uname = input("Enter your username: ")
        pword = input("Enter your password: ")

    print("You have successfully logged in.")
    settings.signedIn = True                 # flags that a user is now signed in
    settings.signedInUname = uname           # tracks the logged in user's username
    settings.currentState = states.mainMenu  # returns to incollege.py's main() w/ currentState = mainMenu


def logOutUser():
    print("Logging Out")
    settings.currentState = states.loggedOut
    settings.signedInUname = None
    settings.signedIn = False
    return True


def findUser(dbCursor):
    # Added the user prompt for searched person within this function
    name = input("Enter the name of a person you know: ").split(" ")
    while len(name) != 2:
        print("Name must be in the form (firstname lastname)")
        name = input("Enter the name of a person you know: ").split(" ")

    first = name[0]
    last = name[1]

    result = db.getUserByFullName(dbCursor, first, last)
    # If the desired user is found successfully, return their data and jump to appropriate menu
    if result is not None:
        print("They are a part of the InCollege system!")
        if settings.signedIn:                         # if a user is signed in
            settings.currentState = states.mainMenu   # returns to incollege.py's main() w/ currentState = mainMenu
            return True
        else:                                         # else a user is not signed in
            settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
            return True
    else:
        while settings.currentState == states.userSearch:
            print("They are not yet a part of the InCollege system yet.")
            print("Options:\n")
            print("1. Search for another user")
            print("2. Return to previous menu")
            response = input()
            if response == '1':
                break
            elif response == '2':
                settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
                return False  # Didn't find user
            else:
                print("Invalid input")


def postJob(dbCursor):
    if db.getNumJobs(dbCursor) >= 5:  # checks if number of jobs in database is at max limit
        print("All permitted jobs have been created, please come back later")
        settings.currentState = states.mainMenu
        return

    # Take input from user and create job in DB
    User = namedtuple('User', 'uname pword firstname lastname')
    currentUser = User._make(db.getUserByName(dbCursor, settings.signedInUname))

    first = currentUser.firstname
    last = currentUser.lastname
    author = first + " " + last
    title = input("Enter job title: ")
    desc = input("Enter job description: ")
    emp = input("Enter employer name: ")
    loc = input("Enter job location: ")
    sal = input("Enter salary: ")

    db.insertJob(dbCursor, title, desc, emp, loc, sal, author)
    print("Job has been posted\n")
    settings.currentState = states.mainMenu  # returns to incollege.py's main() w/ currentState = mainMenu
