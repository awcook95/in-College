from datetime import date, datetime

import database as db
import settings


def printJobMenuNotifications(dbCursor, dbConnection):
    print("Notifications:")
    new_jobs_notifications = db.getNotificationsForUserByType(dbCursor, "new_job", settings.signedInUname)
    jobs_deleted_notifications = db.getNotificationsForUserByType(dbCursor, "job_deleted", settings.signedInUname)
    if len(new_jobs_notifications) == 0 and len(jobs_deleted_notifications) == 0:
        print("No current notifications.")

    # notifications for new jobs posted
    if len(new_jobs_notifications) > 0:
        for n in new_jobs_notifications:
            print(f"A new job '{n[2]}' has been posted.")
            db.deleteNotification(dbCursor, n[1], n[2], n[3])
            dbConnection.commit()

    # notifications for applied-for jobs getting deleted
    if len(jobs_deleted_notifications) > 0:
        for n in jobs_deleted_notifications:
            print(f"A job that you applied for has been deleted - '{n[2]}'.")
            db.deleteNotification(dbCursor, n[1], n[2], n[3])
            dbConnection.commit()

    appliedJobs = len(db.getAppliedJobs(dbCursor, settings.signedInUname))
    if appliedJobs == 1:
        print("\nYou have currently applied for 1 job!")
    else:
        print(f"\nYou have currently applied for {appliedJobs} jobs!")


def printMainMenuNotifications(dbCursor, dbConnection):
    today = date.today()  # Get today's date
    date_format = "%Y-%m-%d %H:%M:%S"
    todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
    currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string
    noJobNotification = ""

    if db.getJobAppliedDate(dbCursor, settings.signedInUname) is None:
        createdDate = db.getUserCreatedDate(dbCursor, settings.signedInUname)
        accountAge = datetime.strptime(createdDate, date_format)  # Date account was created
        age = currentDate - accountAge  # Length of time from account creation and today

        if age.days >= 7:
            noJobNotification = "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
    else:
        newestJob = datetime.strptime(db.getJobAppliedDate(dbCursor, settings.signedInUname), date_format)  # Date of newest applied job
        newestJobAge = currentDate - newestJob  # Length of time from newest applied job and today

        if newestJobAge.days >= 7:
            noJobNotification = "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"

    print("Notifications:")

    # notifications for new students joined
    new_students_notifications = db.getNotificationsForUserByType(dbCursor, "new_student", settings.signedInUname)
    if len(new_students_notifications) > 0:
        for n in new_students_notifications:
            print(f"{n[2]} has joined InCollege.")
            db.deleteNotification(dbCursor, n[1], n[2], n[3])
            dbConnection.commit()

    if noJobNotification != "":
        print(f"\n{noJobNotification}")
