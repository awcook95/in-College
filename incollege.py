import sqlite3
import dbfunctions as db

#program state variables
loggedOut = 0
login = 1
mainMenu = 2
createAccount = 3
selectSkill = 4
quit = 5

state = loggedOut

#connect to database
connection = sqlite3.connect('inCollege.db')

#create cursor
cursor = connection.cursor()

#create tables if none exist
db.initTables(cursor)

print("Welcome to inCollege!")
while(state != quit):
    while(state == loggedOut):
        print("Select Option:")
        print("1. Log in with existing account")
        print("2. Create new account")
        print("3. Quit")
        response = input()
        if response == '1':
            state = login
        elif response == '32':
            state = createAccount
        elif response == '3':
            state = quit
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue
        
    while(state == login):
        #todo - check db for matching uname/pword
        print("Enter your username: ")
        uname = input()
        print("Enter your password: ")
        pword = input()

        if db.tryLogin(cursor, uname, pword):
            print("You have successfully logged in:")
            state = mainMenu
        else:
            print("Incorrect username / password, please try again")

    while(state == createAccount):
        #todo - check if uname already in db
        # check if already 5 accounts and prevent new account if so
        if db.getNumUsers(cursor) >= 5:
            print("All permitted accounts have been created, please come back later" )
            state = loggedOut
            continue

        print("Enter your desired username: ")
        uname = input()
        if db.getUserByName(cursor, uname): #if already exists
            print("Sorry, that username has already been taken")
            continue

        print("Enter your desired password: ")
        pword = input()
        db.insertUser(cursor, uname, pword)
        print("Account has been created")
        state = loggedOut

    while(state == mainMenu):
        print("""Options:
        1. Search for a job/internship
        2. Find someone you know
        3. Learn a new skill
        4. Logout
        """)
        response = input()
        if response == '1':
            print("Under Construction")
        elif response == '2':
            print("Under Construction")
        elif response == '3':
            state = selectSkill
        elif response == '4':
            print("Logging Out")
            state = loggedOut
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue

    while(state == selectSkill):
        print("""What skill would you like to learn?:
        1. Python
        2. How to make a resume
        3. Scrum
        4. Jira
        5. Software Engineering
        6. None - return to menu
        """)
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
            state = mainMenu
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue

print("Ending Program")

connection.commit()
connection.close()
