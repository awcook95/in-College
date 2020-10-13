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
    db.insertUserSettings(dbCursor, uname, settings.emailNotif, settings.smsNotif, settings.targetAdvert, settings.language)
    db.insertProfilePage(dbCursor, uname, "", "", "")
    connection.commit()  # commits the new account and settings to the database (ensures account and settings are saved)

    settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut

    print("Account has been created")


def loginUser(dbCursor):
    # todo: possibly add exit option in case user wants to cancel account login

    uname = input("Enter your username: ")
    pword = input("Enter your password: ")

    while not db.tryLogin(dbCursor, uname, pword):
        print("Incorrect username / password, please try again\n")
        uname = input("Enter your username: ")
        pword = input("Enter your password: ")

    # read in user settings on login
    settings.signedInUname = uname # tracks the logged in user's username
    User = namedtuple('User', 'uname emailnotif smsnotif targetadvert languagepref')
    currentUser = User._make(db.getUserSettingsByName(dbCursor, settings.signedInUname))

    settings.emailNotif = currentUser.emailnotif
    settings.smsNotif = currentUser.smsnotif
    settings.targetAdvert = currentUser.targetadvert
    settings.language = currentUser.languagepref

    settings.signedIn = True                 # flags that a user is now signed in
    settings.currentState = states.mainMenu  # returns to incollege.py's main() w/ currentState = mainMenu

    print("You have successfully logged in.")


def logOutUser():
    print("Logging Out")
    settings.currentState = states.loggedOut
    settings.signedInUname = None
    settings.signedIn = False
    return True


def findUser(dbCursor, connection):
    # Added the user prompt for searched person within this function
    name = input("Enter the name of a person you know: ").split(" ")
    
    # If the user enters an extra spaces at the end of first or last name they will be removed 
    while("" in name):
        name.remove("")

    while len(name) != 2:
        print("Name must be in the form (firstname lastname)")
        name = input("Enter the name of a person you know: ").split(" ")

    first = name[0]
    last = name[1]

    result = db.getUserByFullName(dbCursor, first, last) # Find reciever for friend request

    # If the desired user is found successfully, return their data and jump to appropriate menu
    if result is not None:
        print("They are a part of the InCollege system!")
        User = namedtuple('User', 'uname pword firstname lastname')
        reciever = User._make(result)

        if settings.signedIn:         # if a user is signed in
            if settings.signedInUname != reciever.uname: # Person you are requesting is not yourself
                response = input("Would you like to add them as a friend? Enter 'Y' for yes: ")
                if response.upper() == "Y":
                    # Send request if there is no pending request
                    if not utils.checkExistingFriendRequest(dbCursor, settings.signedInUname, reciever.uname):
                        print("Sending friend request! They will need to accept before they appear in your friends list!")
                        db.insertFriendRequest(dbCursor, settings.signedInUname, reciever.uname)
                        connection.commit()
                    else: 
                        print(reciever.uname + " has already been sent a request! They will show up in your friends list once they accept!")
            
            settings.currentState = states.mainMenu   # returns to incollege.py's main() w/ currentState = mainMenu
            return True
        else:                                         # else a user is not signed in
            settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
            return True
    else:
        while settings.currentState == states.userSearch:
            print("They are not yet a part of the InCollege system yet.")
            print("Options:\n")
            print("A. Search for another user")
            print("B. Return to previous menu")
            response = input()
            if response.upper() == "A":
                break
            elif response.upper() == "B":
                if settings.signedIn:
                    settings.currentState = states.mainMenu
                else:
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


def changeUserSettings(dbCursor, connection):
    while settings.currentState == states.modifyUserSettings:
        print("A. Email Notifications\n"
              "B. SMS Notifications\n"
              "C. Targeted Advertising\n"
              "Z. Return to previous menu")
        response = input("Select a setting to modify: ")
        if response.upper() == "A":
            option = input("Email Notifications - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.emailNotif = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "B":
            option = input("SMS Notifications - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.smsNotif = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "C":
            option = input("Targeted Advertising - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.targetAdvert = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "Z":
            if settings.signedIn:
                db.updateUserSettings(dbCursor, settings.signedInUname, settings.emailNotif, settings.smsNotif, settings.targetAdvert)
                connection.commit()
                print("Settings successfully saved.")
            settings.currentState = states.importantLinks
        else:
            print("Invalid Option, enter the letter option you want and press enter")
