import sqlite3

import dbfunctions as db

# session state variable 
signedIn = False

# program state variables
loggedOut = 0
login = 1
mainMenu = 2
createAccount = 3
selectSkill = 4
quit = 5
findUser = 6

state = loggedOut

# connect to database
connection = sqlite3.connect('inCollege.db')

# create cursor
cursor = connection.cursor()

# create tables if none exist
db.initTables(cursor)


# function to validate password 
def validatePassword(password):
    if len(password) < 8 or len(password) > 12:     # out of length bounds
        return False
    elif not any(x.isupper() for x in password):    # no capital letter
        return False
    elif not any(x.isnumeric() for x in password):  # no digits
        return False
    elif not any(x.isalnum() for x in password):    # non alphanumeric
        return False
    else:
        return True


def enterInitialMenu():
    global state

    while state == loggedOut:
        print("Select Option:")
        print("1. Log in with existing account")
        print("2. Create new account")
        print("3. Search for a job")
        print("4. Learn a new skill")
        print("5. Find someone you know")
        print("6. Quit")
        response = input()
        if response == '1':
            state = login
        elif response == '2':
            state = createAccount
        elif response == '3':
            print("Under Construction")
        elif response == '4':
            state = selectSkill
        elif response == '5':
            state = findUser
        elif response == '6':
            state = quit
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue

def findUser(dbCursor, first, last):
        global state
        result = db.getUserByFullName(dbCursor, first, last)

        if result != None:
            print("They are a part of the InCollege system!")
            if(signedIn):
                enterMainMenu(dbCursor)
                return True
            else:
                enterInitialMenu()
                return True
        else:
            while(state == findUser):
                print("They are not yet a part of the InCollege system yet.")
                print("Options:\n")
                print("1. Search for another user")
                print("2. Return to previous menu")
                response = input()
                if(response == '1'):
                    break
                elif(response == '2'):
                    state = loggedOut
                    return False # Didn't find user
                else:
                    print("Invalid input")



def loginUser(dbCursor):
    global state
    global signedIn  # added

    # todo: add exit option in case user wants to cancel account login

    uname = input("Enter your username: ")
    pword = input("Enter your password: ")

    if not db.tryLogin(dbCursor, uname, pword):
        print("Incorrect username / password, please try again")
        state = loggedOut
        return

    print("You have successfully logged in.")
    signedIn = True  # added
    state = mainMenu

def logOutUser(signedIn):
    if(signedIn):
        print("Logging Out")
        state = loggedOut
        signedIn = False
        return True
    else:
        return False


def createUser(dbCursor):
    global signedIn
    global state

    # todo: add exit option in case user wants to cancel account creation

    if db.getNumUsers(dbCursor) >= 5:  # checks if number of accounts in database is at max limit
        print("All permitted accounts have been created, please come back later")
        state = loggedOut
        signedIn = False
        return 

    uname = input("Enter your desired username: ")
    # added below if statement to return back to main menu if username is taken
    if db.getUserByName(dbCursor, uname):
        print("Sorry, that username has already been taken")
        state = loggedOut
        return

    pword = input("Enter your desired password: ")
    while not validatePassword(pword):
        print("Invalid password. Must be length 8-12 characters, contain one digit, one uppercase character, and one non-alphanumeric")
        pword = input("Enter your desired password: ")

    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")

    db.insertUser(dbCursor, uname, pword, fname, lname)
    print("Account has been created")
    state = loggedOut
    signedIn = False
    connection.commit()


def enterMainMenu(dbCursor):
    global signedIn
    global state

    while state == mainMenu:
        print("Options:\n"
              "1. Search for a job/internship\n"
              "2. Find someone you know\n"
              "3. Learn a new skill\n"
              "4. Logout")
        response = input()
        if response == '1':
            print("Under Construction")
        elif response == '2':
            state = findUser
            while (state == findUser):
                print("Enter the name of a person you know: ")
                name = input()
                name = name.split(" ")
                if len(name) != 2:
                    print("Name must be in the form (firstname lastname)")
                    continue

                first = name[0]
                last = name[1]
            findUser(dbCursor, first, last)
            state = mainMenu
        elif response == '3':
            state = selectSkill
        elif response == '4':
            global signedIn
            logOutUser(signedIn)
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


def enterSkillMenu():
    global state

    while state == selectSkill:
        print("What skill would you like to learn?:\n"
              "1. Python\n"
              "2. How to make a resume\n"
              "3. Scrum\n"
              "4. Jira\n"
              "5. Software Engineering\n"
              "6. None - return to menu")
        response = input()
        if response == '1':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '2':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '3':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '4':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '5':
            print("Under Construction")
            return True # Searched for skill successfully
        elif response == '6':
            if not signedIn:
                state = loggedOut
            else:
                state = mainMenu
            return False # Dont learn skill
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


def main(dbCursor):
    global signedIn
    global state

    print("Welcome to inCollege!")
    while state != quit:
        if state == loggedOut:
            enterInitialMenu()

        if state == login:
            loginUser(dbCursor)

        if state == createAccount:
            createUser(dbCursor)

        if state == mainMenu:
            enterMainMenu(dbCursor)

        if state == selectSkill:
            enterSkillMenu()

        if state == findUser:
            print("Enter the name of a person you know: ")
            name = input()
            name = name.split(" ")
            if len(name) != 2:
                print("Name must be in the form (firstname lastname)")
                continue

            first = name[0]
            last = name[1]
            findUser(dbCursor, first, last)

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor)
