import database as db
import settings


def printJobNotifications(dbCursor, dbConnection):
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
