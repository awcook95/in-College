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

    # dictionary to hold states and their corresponding function names
    # every state added must have their corresponding function take (dbCursor, dbConnection) as arguments
    options = {
        states.loggedOut:          ui.enterInitialMenu,
        states.login:              users.loginUser,
        states.createAccount:      users.createUser,
        states.mainMenu:           ui.enterMainMenu,
        states.selectSkill:        ui.enterSkillMenu,
        states.userSearch:         users.findUser,
        states.createJob:          users.postJob,
        states.apply:              users.applyForJob,
        states.viewJobs:           ui.printJobListings,
        states.deleteJob:          ui.enterDeleteAJobMenu,
        states.favoriteJob:        users.favoriteAJob,
        states.viewFavoriteJobs:   ui.viewFavoriteJobs,
        states.viewAppliedJobs:    ui.viewAppliedJobs,
        states.viewUnappliedJobs:  ui.viewUnappliedJobs,
        states.jobMenu:            ui.enterJobMenu,
        states.usefulLinks:        ui.usefulLinksMenu,
        states.general:            ui.generalMenu,
        states.browseInCollege:    ui.browseMenu,
        states.businessSolutions:  ui.solutionsMenu,
        states.directories:        ui.directoriesMenu,
        states.importantLinks:     ui.enterImportantLinksMenu,
        states.modifyUserSettings: users.changeUserSettings,
        states.friendsMenu:        ui.enterFriendsMenu,
        states.profilePage:        ui.enterProfilePageMenu,
        states.messageCenter:      ui.messageCenterMenu,
        states.inbox:              ui.inboxMenu,
        states.sendMessage:        ui.sendMessageMenu
    }

    while settings.currentState != states.quit:  # this while loop handles every state and calls corresponding methods
        options[settings.currentState](dbCursor, dbConnection)

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor, connection)
