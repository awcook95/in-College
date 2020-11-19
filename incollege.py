import sqlite3
from datetime import datetime, date

import database as db
import jobs
import messages
import profiles
import settings
import states
import ui
import users
import training
import API

# connect to database
connection = sqlite3.connect('inCollege.db')

# create cursor
cursor = connection.cursor()

# create tables if none exist
db.initTables(cursor)


def main(dbCursor, dbConnection):
    # NEED TO CREATE TABLE TO STORE TRAINING DATA 

    today = date.today()  # Get today's date
    date_format = "%m/%d/%Y"
    todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
    currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string

    # Run all input API calls
    # Create users
    user_count = db.getNumUsers(dbCursor)
    student_accounts = API.createStudentAccounts()
    for obj in student_accounts:
        # only create up to 10 accounts, don't recreate accounts
        if user_count <= 10 and db.getUserByFullName(dbCursor, obj.first_name, obj.last_name) == None: 
            db.insertUser(dbCursor, obj.username, obj.password, obj.first_name, obj.last_name, obj.plus_member, currentDate)
            user_count += 1
        else: 
            break
    dbConnection.commit() 

    # Create jobs
    job_count = db.getNumJobs(dbCursor)
    new_jobs = API.createJobs()
    for obj in new_jobs:
        # job limit is 10, don't recreate jobs
        if job_count <= 10 and db.getJobByTitle(dbCursor, obj.title) == None:
            # ADDING UNKOWN AUTHOR FOR NOW
            db.insertJob(dbCursor, obj.title, obj.description, obj.employer_name, obj.location, obj.salary, "Unkown Author")
        else: 
            break
    dbConnection.commit()

    # trainings = API.createTrainings()
    # if trainings:
    #     for obj in trainings:
    #         print(obj)
    #     print("\n")

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
        states.createJob:          jobs.postJob,
        states.viewJobs:           jobs.enterViewJobsMenu,
        states.deleteJob:          jobs.enterDeleteAJobMenu,
        states.jobMenu:            jobs.enterJobMenu,
        states.usefulLinks:        ui.usefulLinksMenu,
        states.general:            ui.generalMenu,
        states.browseInCollege:    ui.browseMenu,
        states.businessSolutions:  ui.solutionsMenu,
        states.directories:        ui.directoriesMenu,
        states.importantLinks:     ui.enterImportantLinksMenu,
        states.modifyUserSettings: users.changeUserSettings,
        states.friendsMenu:        ui.enterFriendsMenu,
        states.profilePage:        profiles.enterProfilePageMenu,
        states.messageCenter:      messages.messageCenterMenu,
        states.inbox:              messages.inboxMenu,
        states.sendMessage:        messages.sendMessageMenu,
        states.training:           training.trainingMenu,
        states.learning:           training.enterLearningMenu
    }

    while settings.currentState != states.quit:  # this while loop handles every state and calls corresponding methods
        options[settings.currentState](dbCursor, dbConnection)

    print("Ending Program")

    # This needs to happen for changes to be committed to db
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main(cursor, connection)
