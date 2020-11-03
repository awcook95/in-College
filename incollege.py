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


def main(dbCursor, dbConnection):
    # This menu will run all main functionality
    print("Welcome to inCollege!")
    while settings.currentState != states.quit:  # this while loop handles every state and calls corresponding methods
        if settings.currentState == states.loggedOut:
            ui.enterInitialMenu()

        if settings.currentState == states.login:
            users.loginUser(dbCursor)

        if settings.currentState == states.createAccount:
            users.createUser(dbCursor, dbConnection)

        if settings.currentState == states.mainMenu:
            ui.enterMainMenu(dbCursor, dbConnection)

        if settings.currentState == states.selectSkill:
            ui.enterSkillMenu()
            
        if settings.currentState == states.userSearch:
            users.findUser(dbCursor, dbConnection)
                  
        if settings.currentState == states.createJob:
            users.postJob(dbCursor, dbConnection)

        if settings.currentState == states.apply:
            users.applyForJob(dbCursor, dbConnection)
             
        if settings.currentState == states.viewJobs: 
            ui.printJobListings(dbCursor, dbConnection)
        
        if settings.currentState == states.deleteJob: 
            ui.enterDeleteAJobMenu(dbCursor, dbConnection)

        if settings.currentState == states.favoriteJob: 
            users.favoriteAJob(dbCursor, dbConnection)

        if settings.currentState == states.viewFavoriteJobs: 
            ui.viewFavoriteJobs(dbCursor, dbConnection)

        if settings.currentState == states.viewAppliedJobs: 
            ui.viewAppliedJobs(dbCursor, dbConnection)

        if settings.currentState == states.viewUnappliedJobs: 
            ui.viewUnappliedJobs(dbCursor, dbConnection)
            
        if settings.currentState == states.jobMenu: 
            ui.enterJobMenu()
            
        if settings.currentState == states.usefulLinks:
            ui.usefulLinksMenu()
        
        if settings.currentState == states.general:
            ui.generalMenu()
            
        if settings.currentState == states.browseInCollege:
            ui.browseMenu()
            
        if settings.currentState == states.businessSolutions:
            ui.solutionsMenu()
            
        if settings.currentState == states.directories:
            ui.directoriesMenu()

        if settings.currentState == states.importantLinks:
            ui.enterImportantLinksMenu(dbCursor, dbConnection)

        if settings.currentState == states.modifyUserSettings:
            users.changeUserSettings(dbCursor, dbConnection)

        if settings.currentState == states.friendsMenu:
            ui.enterFriendsMenu(dbCursor, dbConnection)

        if settings.currentState == states.profilePage:
            ui.enterProfilePageMenu(dbCursor, dbConnection)

        if settings.currentState == states.messageCenter:
            ui.messageCenterMenu(dbCursor, dbConnection) #### NEW EPIC 7 ####

        if settings.currentState == states.inbox:
            ui.inboxMenu(dbCursor, dbConnection) #### NEW EPIC 7 ####
        
        if settings.currentState == states.sendMessage:
            ui.sendMessageMenu(dbCursor, dbConnection) #### NEW EPIC 7 ####

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor, connection)
