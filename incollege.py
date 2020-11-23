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


# Create users
def inputAPIUsers(dbCursor, dbConnection):
    today = date.today()  # Get today's date
    date_format = "%m/%d/%Y"
    todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
    currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string

    user_count = db.getNumUsers(dbCursor)
    student_accounts = API.createStudentAccounts()
    if student_accounts:
        for obj in student_accounts:
            # only create up to 10 accounts, don't recreate accounts
            if user_count < 10 and db.getUserByFullName(dbCursor, obj.first_name, obj.last_name) is None:
                db.insertUser(dbCursor, obj.username, obj.password, obj.first_name, obj.last_name, obj.plus_member, currentDate)
                db.insertUserSettings(dbCursor, obj.username, settings.emailNotif, settings.smsNotif, settings.targetAdvert, settings.language)
                db.insertProfilePage(dbCursor, obj.username, "", "", "")
                user_count += 1

    dbConnection.commit()


# Create jobs
def inputAPIJobs(dbCursor, dbConnection):
    job_count = db.getNumJobs(dbCursor)
    new_jobs = API.createJobs()
    if new_jobs:
        for obj in new_jobs:
            # job limit is 10, don't recreate jobs
            if job_count < 10 and db.getJobByTitle(dbCursor, obj.title) is None:
                # ADDING UNKNOWN AUTHOR FOR NOW
                db.insertJob(dbCursor, obj.title, obj.description, obj.employer_name, obj.location, obj.salary, "Unknown Author")
    dbConnection.commit()


# Create trainings
def inputAPITrainings(dbCursor, dbConnection):
    trainings = API.createTrainings()
    if trainings:
        for obj in trainings:
            if db.getTrainingByTitle(dbCursor, obj) is None:
                db.insertNewTraining(dbCursor, obj)
    dbConnection.commit()


def main(dbCursor, dbConnection):
    # Input API functions
    inputAPIUsers(dbCursor, dbConnection)
    inputAPIJobs(dbCursor, dbConnection)
    inputAPITrainings(dbCursor, dbConnection)

    API.outputAppliedJobs(dbCursor)      # output applied jobs
    API.outputSavedJobsByUser(dbCursor)  # output saved jobs
    API.outputJobs(dbCursor)             # output all jobs
    API.outputProfiles(dbCursor)         # output user profiles
    API.outputUsers(dbCursor)            # output all users

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
