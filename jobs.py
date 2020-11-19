from collections import namedtuple
from datetime import datetime, date

import constants
import database as db
import notifications
import settings
import states
import API


def enterJobMenu(dbCursor, dbConnection):
    notifications.printJobMenuNotifications(dbCursor, dbConnection)

    print("\nSelect a job function:\n"
          "A. Post Job\n"
          "B. Delete Job\n"
          "C. View Jobs\n" 
          "Z. Return to Previous Menu")
    while settings.currentState == states.jobMenu:
        choice = input("Input: ")
        if choice.upper() == "A":
            settings.currentState = states.createJob  # returns to main() w/ currentState = createJob
        elif choice.upper() == "B":
            settings.currentState = states.deleteJob
        elif choice.upper() == "C":
            settings.currentState = states.viewJobs
        elif choice.upper() == "Z":
            settings.currentState = states.mainMenu   # returns to main() w/ currentState = mainMenu
        else:
            print(constants.INVALID_INPUT)


def postJob(dbCursor, dbConnection):
    if db.getNumJobs(dbCursor) >= constants.MAX_POSTED_JOBS:  # checks if number of jobs in database is at max limit
        print("All permitted jobs have been created, please come back later.")
        settings.currentState = states.jobMenu
        return

    # Take input from user and create job in DB
    User = namedtuple('User', 'uname pword firstname lastname plusMember date_created')
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

    # add notification to let other users know a job has been posted
    other_users = db.getAllOtherUsers(dbCursor, settings.signedInUname)
    if len(other_users) > 0:
        for user in other_users:
            db.insertNotification(dbCursor, "new_job", title, user[0])

    dbConnection.commit()
    API.outputJobs(dbCursor)
    print("Job has been posted.")
    settings.currentState = states.jobMenu  # returns to main() w/ currentState = jobMenu


def enterDeleteAJobMenu(dbCursor, dbConnection):
    jobs = db.getJobsPostedByUser(dbCursor, db.getUserFullName(dbCursor, settings.signedInUname))

    print()
    if len(jobs) > 0:
        print("Your Posted Jobs:")
        for i in range(len(jobs)):
            print(f"{i + 1}. {(jobs[i])[1]}")
    else:
        print("You have not posted any jobs yet! You can only delete jobs that you have posted.")
        settings.currentState = states.jobMenu
        return

    print("\n Choose one of the above jobs to delete (job #)")
    print("Z. Return to Previous Menu")

    while True:
        response = input("Input: ")
        if response.isdigit() and 1 <= int(response) <= len(jobs):
            selectedJob = jobs[int(response) - 1]

            # add notification to let job applicants that the job was deleted
            job_applicants = db.getJobApplicantsByTitle(dbCursor, selectedJob[1])
            if len(job_applicants) > 0:
                for applicant in job_applicants:
                    db.insertNotification(dbCursor, "job_deleted", selectedJob[1], applicant[0])

            # todo: delete job applications for job to be deleted

            db.deleteJob(dbCursor, selectedJob[0])
            dbConnection.commit()
            print("Successfully deleted job.")
            break
        elif response.upper() == "Z":
            settings.currentState = states.jobMenu
            return
        else:
            print(constants.INVALID_INPUT)


def enterViewJobsMenu(dbCursor, dbConnection):
    print("\nChoose filter:\n"
          "A. View All Jobs\n"
          "B. View Favorite Jobs\n"
          "C. View Jobs Applied To\n"
          "D. View Jobs Not Applied To\n"
          "Z. Return to Previous Menu")
    while settings.currentState == states.viewJobs:
        response = input("Input: ")
        if response.upper() == "A":
            printJobsWithFilter(dbCursor, dbConnection, 0)
            break
        elif response.upper() == "B":
            printJobsWithFilter(dbCursor, dbConnection, 1)
            break
        elif response.upper() == "C":
            printJobsWithFilter(dbCursor, dbConnection, 2)
            break
        elif response.upper() == "D":
            printJobsWithFilter(dbCursor, dbConnection, 3)
            break
        elif response.upper() == "Z":
            settings.currentState = states.jobMenu
        else:
            print(constants.INVALID_INPUT)


def printJobsWithFilter(dbCursor, dbConnection, filterOption):
    while True:
        jobs = None
        title = ""
        if filterOption == 0:
            jobs = db.getAllJobs(dbCursor)
            title = "All Jobs:"
        elif filterOption == 1:
            jobs = db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)
            title = "Favorite Jobs:"
        elif filterOption == 2:
            jobs = db.getAppliedJobs(dbCursor, settings.signedInUname)
            title = "Jobs Applied To:"
        elif filterOption == 3:
            jobs = db.getUnappliedJobs(dbCursor, settings.signedInUname)
            title = "Jobs Not Applied To:"

        print()
        if len(jobs) > 0:
            print(title)
            for i in range(len(jobs)):
                if len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, (jobs[i])[1])) > 0:  # if user has applied to this job
                    print(f"{i + 1}. {(jobs[i])[1]} (Applied)")
                else:
                    print(f"{i + 1}. {(jobs[i])[1]}")
        else:
            print("No jobs available under this filter.")
            return

        print("#. Choose one of the above jobs to view details")
        print("Z. Return to Previous Menu")

        while True:
            response = input("Input: ")
            if response.isdigit() and 1 <= int(response) <= len(jobs):
                selectedJob = jobs[int(response) - 1]
                viewJobDetails(dbCursor, dbConnection, selectedJob)
                break
            elif response.upper() == "Z":
                return
            else:
                print(constants.INVALID_INPUT)


def viewJobDetails(dbCursor, dbConnection, selectedJob):
    while True:
        print(f"\nTitle: {selectedJob[1]}")
        print(f"\tDescription: {selectedJob[2]}")
        print(f"\tEmployer: {selectedJob[3]}")
        print(f"\tLocation: {selectedJob[4]}")
        print(f"\tSalary: {selectedJob[5]}")
        print(f"\tJob Poster: {selectedJob[6]}")
        print("A. Apply For Job")
        if any(selectedJob[0] in job for job in db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)):
            print("B. Unfavorite Job")
        else:
            print("B. Favorite Job")
        print("Z. Return to Previous Menu")
        while True:
            response = input("Input: ")
            if response.upper() == "A":
                applyForJob(dbCursor, dbConnection, selectedJob)
                break
            elif response.upper() == "B":
                if any(selectedJob[0] in job for job in db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)):
                    db.deleteFavoriteJob(dbCursor, settings.signedInUname, selectedJob[1])
                    print("Job removed from favorites.")
                else:
                    db.insertFavoriteJob(dbCursor, settings.signedInUname, selectedJob[1])
                    print("Job added to favorites.")
                break
            elif response.upper() == "Z":
                return
            else:
                print(constants.INVALID_INPUT)


def applyForJob(dbCursor, dbConnection, job):
    if len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, job[1])) > 0:
        print("You have already applied for this job!")
        return

    if job in db.getJobsPostedByUser(dbCursor, db.getUserFullName(dbCursor, settings.signedInUname)):
        print("You cannot apply for a job that you posted!")
        return

    grad = input("Please enter your graduation date (mm/dd/yyyy): ")
    start = input("Please enter the earliest date you can start (mm/dd/yyyy): ")
    credentials = input("Please briefly describe why you are fit for this job: ")
    today = date.today()  # Get today's date
    date_format = "%m/%d/%Y"
    todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
    currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string
    db.insertUserJobApplication(dbCursor, settings.signedInUname, job[1], grad, start, credentials, currentDate)
    dbConnection.commit()
    print("Successfully applied for job.")
