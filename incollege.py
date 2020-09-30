import sqlite3

import dbfunctions as db
import settings
import states
import ui
import users

# connect to database
connection = sqlite3.connect('inCollege.db')

# create cursor
cursor = connection.cursor()

# create tables if none exist
db.initTables(cursor)


def main(dbCursor):
    # This menu will run all main functionality 
    print("Welcome to inCollege!\n")
    while settings.currentState != states.quit:
        if settings.currentState == states.loggedOut:
            ui.enterInitialMenu()

        if settings.currentState == states.login:
            users.loginUser(dbCursor)

        if settings.currentState == states.createAccount:
            users.createUser(dbCursor, connection)

        if settings.currentState == states.mainMenu:
            ui.enterMainMenu()

        if settings.currentState == states.selectSkill:
            ui.enterSkillMenu()
            
        if settings.currentState == states.userSearch:
            users.findUser(dbCursor)
                  
        if settings.currentState == states.createJob:
            users.postJob(dbCursor)

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor)
