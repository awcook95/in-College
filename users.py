from collections import namedtuple
from datetime import datetime, date

import constants
import database as db
import settings
import states
import utils


def createUser(dbCursor, connection):
    if db.getNumUsers(dbCursor) >= constants.MAX_USER_ACCOUNTS:  # checks if number of accounts in database is at max limit
        print("All permitted accounts have been created, please come back later")
        settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut
        return

    print("Enter desired account credentials, or only press enter at any time to cancel account creation.")
    uname = input("Enter your desired username: ")
    if uname == "":
        print("Account creation canceled.")
        return

    while db.getUserByName(dbCursor, uname):
        print("Sorry, that username has already been taken.")
        uname = input("Enter your desired username: ")
        if uname == "":
            print("Account creation canceled.")
            return

    pword = input("Enter your desired password: ")
    if pword == "":
        print("Account creation canceled.")
        return

    while not utils.validatePassword(pword):
        print("Invalid password. Must be length 8-12 characters, contain one digit, one uppercase character, and one non-alphanumeric.")
        pword = input("Enter your desired password: ")
        if pword == "":
            print("Account creation canceled.")
            return

    fname = input("Enter your first name: ")
    if fname == "":
        print("Account creation canceled.")
        return

    lname = input("Enter your last name: ")
    if lname == "":
        print("Account creation canceled.")
        return

    plusMember = input("Sign up for InCollege-Plus membership? (Enter Y for Plus, N for Standard): ")
    while True:
        if plusMember.upper() == "Y":
            plusMember = 1
            break
        elif plusMember.upper() == "N":
            plusMember = 0
            break
        else:
            print(constants.INVALID_INPUT)
            plusMember = input("Sign up for InCollege-Plus membership? (Enter Y for Plus, N for Standard): ")

    today = date.today()  # Get today's date
    date_format = "%m/%d/%Y"
    todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
    currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string

    db.insertUser(dbCursor, uname, pword, fname, lname, plusMember, currentDate)
    db.insertUserSettings(dbCursor, uname, settings.emailNotif, settings.smsNotif, settings.targetAdvert, settings.language)
    db.insertProfilePage(dbCursor, uname, "", "", "")

    # add notification to let other users know a new student has joined
    other_users = db.getAllOtherUsers(dbCursor, uname)
    if len(other_users) > 0:
        for user in other_users:
            db.insertNotification(dbCursor, "new_student", fname + " " + lname, user[0])

    connection.commit()  # commits the new account and settings to the database (ensures account and settings are saved)

    settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut

    print("Account has been created.")


def loginUser(dbCursor, dbConnection):
    print("Enter login information, or press enter twice to cancel.")
    uname = input("Enter your username: ")
    pword = input("Enter your password: ")

    if uname == "" and pword == "":
        print("Account login canceled.")
        settings.currentState = states.loggedOut
        return

    while not db.tryLogin(dbCursor, uname, pword):
        print("Incorrect username / password, please try again.")
        print("Enter login information, or press enter twice to cancel.")
        uname = input("Enter your username: ")
        pword = input("Enter your password: ")

        if uname == "" and pword == "":
            print("Account login canceled.")
            settings.currentState = states.loggedOut
            return

    # read in user settings on login
    settings.signedInUname = uname  # tracks the logged in user's username
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
    result = None
    while settings.currentState == states.userSearch:
        # Added the user prompt for searched person within this function
        print("Which search term do you want to find users by?")
        print("A. By Full Name")
        print("B. By Last Name")
        print("C. By University")
        print("D. By Major")
        print("Z. Return to Previous Menu")
        response = input("Enter how you wish to search for a user: ")
        if response.upper() == 'A':
            name = input("Enter the name of a person you know: ").split(" ")

            # If the user enters an extra spaces at the end of first or last name they will be removed
            while "" in name:
                name.remove("")

            while len(name) != 2:
                print("Name must be in the form (firstname lastname)")
                name = input("Enter the name of a person you know: ").split(" ")

            first = name[0]
            last = name[1]

            result = db.getUserByFullName(dbCursor, first, last)  # Find receiver for friend request
            break
        elif response.upper() == 'B':
            name = input("Enter the last name of the person you might know: ")
            users_found = utils.printUsersFoundLastName(dbCursor, name)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        first_name = (users_found[int(response) - 1])[2]  # parse first name from user object
                        last_name = (users_found[int(response) - 1])[3]   # parse last name from user object
                        result = db.getUserByFullName(dbCursor, first_name, last_name)
                        break
                    else:
                        print(constants.INVALID_INPUT)
            break
        elif response.upper() == 'C':
            university = input("Enter the University of the person you might know goes to: ")
            users_found = utils.printUsersFoundParameter(dbCursor, university, 0)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        name = db.getUserByName(dbCursor, (users_found[int(response) - 1])[0])  # parses first and last name from user object
                        result = db.getUserByFullName(dbCursor, name[2], name[3])
                        break
                    else:
                        print(constants.INVALID_INPUT)
            break
        elif response.upper() == 'D':
            major = input("Enter the major of the person you might know has: ")
            users_found = utils.printUsersFoundParameter(dbCursor, major, 1)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        name = db.getUserByName(dbCursor, (users_found[int(response) - 1])[0])  # parses first and last name from user object
                        result = db.getUserByFullName(dbCursor, name[2], name[3])
                        break
                    else:
                        print(constants.INVALID_INPUT)
            break
        elif response.upper() == 'Z':
            if settings.signedIn:
                settings.currentState = states.mainMenu
            else:
                settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut
            return False  # Didn't find user
        else:
            print(constants.INVALID_INPUT)

    # If the desired user is found successfully, return their data and jump to appropriate menu
    if result is not None:
        User = namedtuple('User', 'uname pword firstname lastname plus_member date_created')
        receiver = User._make(result)
        if settings.signedIn:
            friend_exists = db.checkUserFriendRelation(dbCursor, settings.signedInUname, receiver.uname)

            # If this person is already your friend,return
            if friend_exists:
                print(receiver.uname + " is already your friend!")
                settings.currentState = states.mainMenu   # returns to main() w/ currentState = mainMenu
                return True
        
        print("They are a part of the InCollege system!")
        if settings.signedIn:  # if a user is signed in
            if settings.signedInUname != receiver.uname:  # Person you are requesting is not yourself
                response = input("Would you like to add them as a friend? Enter 'Y' for yes: ")
                request_exists = utils.checkExistingFriendRequest(dbCursor, settings.signedInUname, receiver.uname)
                
                if response.upper() == "Y":
                    # Send request if there is no pending request
                    if not request_exists:
                        print("Sending friend request! They will need to accept before they appear in your friends list!\n")
                        db.insertFriendRequest(dbCursor, settings.signedInUname, receiver.uname)
                        connection.commit()
                    else: 
                        print(receiver.uname + " has already been sent a request! They will show up in your friends list once they accept!")
            
            settings.currentState = states.mainMenu   # returns to main() w/ currentState = mainMenu
            return True
        else:                                         # else a user is not signed in
            settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut
            return True
    else:
        while settings.currentState == states.userSearch:
            print("They are not yet a part of the InCollege system yet.")
            print("Options:")
            print("A. Search for another user")
            print("Z. Return to previous menu")
            response = input("Input: ")
            if response.upper() == "A":
                break
            elif response.upper() == "Z":
                if settings.signedIn:
                    settings.currentState = states.mainMenu
                else:
                    settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut
                return False  # Didn't find user
            else:
                print(constants.INVALID_INPUT)


def changeUserSettings(dbCursor, connection):
    while settings.currentState == states.modifyUserSettings:
        print("A. Email Notifications\n"
              "B. SMS Notifications\n"
              "C. Targeted Advertising\n"
              "Z. Return to Previous Menu")
        response = input("Select a setting to modify: ")
        if response.upper() == "A":
            while True:
                option = input("Email Notifications - enter 1 to turn on or enter 0 to turn off: ")
                if option == "1" or option == "0":
                    settings.emailNotif = option
                    print("Setting changed; return to previous menu if logged in or create an account to save changes.")
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "B":
            while True:
                option = input("SMS Notifications - enter 1 to turn on or enter 0 to turn off: ")
                if option == "1" or option == "0":
                    settings.smsNotif = option
                    print("Setting changed; return to previous menu if logged in or create an account to save changes.")
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "C":
            while True:
                option = input("Targeted Advertising - enter 1 to turn on or enter 0 to turn off: ")
                if option == "1" or option == "0":
                    settings.targetAdvert = option
                    print("Setting changed; return to previous menu if logged in or create an account to save changes.")
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "Z":
            if settings.signedIn:
                db.updateUserSettings(dbCursor, settings.signedInUname, settings.emailNotif, settings.smsNotif, settings.targetAdvert)
                connection.commit()
                print("Settings successfully saved.")
            settings.currentState = states.importantLinks
        else:
            print(constants.INVALID_INPUT)
