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
postJob = 7

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
        # success story
        print("Nathan Cooper had always dreamed about getting a software engineering job after graduating from college.\n"
              "However, with no work history and no connections, he feared that finding a company to hire him after graduation\n"
              "would be difficult. After using inCollege, Nathan was able to connect with other students in the same major to\n"
              "discuss school, jobs, salaries, offers, and projects. He was also able to learn new skills that would increase\n"
              "his experience and improve the look of his resume.\n")
        
        print("Select Option:")
        print("1. Log in with existing account")
        print("2. Create new account")
        print("3. Find someone you know")
        print("4. Play a video")
        print("5. Quit")
        
        response = input()
        if response == '1':
            state = login
        elif response == '2':
            state = createAccount
        elif response == '3':
            state = finduser
        elif response == '4':
            print("Video is now playing\n)
        elif response == '5':
            state = quit
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue

def findUser(dbCursor):
    global state
    
    while(state == findUser):
        print("Enter the name of a person you know: ")
        name = input()
        name = name.split(" ")
        if len(name) != 2:
            print("Name must be in the form (firstname lastname)")
            continue

        first = name[0]
        last = name[1]
        result = db.getUserByFullName(dbCursor, first, last)

        if result != None:
            while(state == findUser):
                print("They are a part of the InCollege system!")
                print("Would you like to join InCollege?")
                print("Options:")
                print("1. Log in with existing account")
                print("2. Create account")
                print("3. Return to previous menu")
                response = input()
                if(response == '1'):
                    state = login
                elif(response == '2'):
                    state = createAccount
                elif(response == '3'):
                    state = loggedOut
                else:
                    print("Invalid input")

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


def enterMainMenu():
    global signedIn
    global state

    while state == mainMenu:
        print("Options:\n"
              "1. Search for a job/internship\n"
              "2. Post a job\n"
              "3. Find someone you know\n"
              "4. Learn a new skill\n"
              "5. Logout")
        response = input()
        if response == '1':
            print("Under Construction")
        elif response == '2':
            state = postJob
        elif response == '3':
            print("Under Construction")
        elif response == '4':
            state = selectSkill
        elif response == '5':
            print("Logging Out")
            state = loggedOut
            signedIn = False
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


def postJob(dbCursor):
    global state
                  
    if db.getNumJobs(dbCursor) >= 5:  # checks if number of jobs in database is at max limit
        print("All permitted jobs have been created, please come back later")
        state = mainMenu
        return
    
    first = input("Enter first name: ")
    last = input("Enter last name: ")              
    author = db.getUserByFullName(dbCursor, first, last)
                  
    if author == None:
       print("There are no accounts with that name, please enter a valid first and last name\n")
       continue
                  
    title = input("Enter job title: ")
    desc = input("Enter job description: ")
    emp = input("Enter employer name: ")
    loc = input("Enter job location: ")
    sal = input("Enter salary: ")
    
    db.insertJob(dbCursor, title, desc, emp, loc, sal, author)
    print("Job has been posted\n")
    state = mainMenu
                  
                  
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
        elif response == '2':
            print("Under Construction")
        elif response == '3':
            print("Under Construction")
        elif response == '4':
            print("Under Construction")
        elif response == '5':
            print("Under Construction")
        elif response == '6':
            if not signedIn:
                state = loggedOut
            else:
                state = mainMenu
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
            enterMainMenu()

        if state == selectSkill:
            enterSkillMenu()

        if state == findUser:
            findUser(dbCursor)
                  
        if state == postJob:
            postJob(dbCursor)

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor)
