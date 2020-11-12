from collections import namedtuple
import constants
import database as db
import notifications
import settings
import states


def printJobListings(dbCursor, dbConnection):
    print("Jobs currently listed in the system:\n")
    jobs = db.getAllJobs(dbCursor)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            if len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, selectedJob.title)) > 0:  # if user has applied to this job
                print(f"{i+1}. Job Title: {selectedJob.title} (Applied)")
            else:
                print(f"{i+1}. Job Title: {selectedJob.title}")
    else:
        input("No jobs have been posted\nPress enter to return to previous menu.")
        settings.currentState = states.jobMenu
        return

    response = input("View Job details (Y/N)? ")
    # print full job details
    while response.upper() == "Y":
        Job = namedtuple('User', 'jobID title description employer location salary author')
        if len(jobs) != 1:
            job_id = input("Which job 1 - " + str(len(jobs)) + " would you like to view? ")
            try:
                int(job_id)
            except ValueError:
                print("Invalid input")
                continue
            if int(job_id) not in range(1, len(jobs) + 1):
                print("Invalid input")
                continue

            selectedJob = Job._make(jobs[int(job_id) - 1])
        else:
            selectedJob = Job._make(jobs[0])

        print(f"Job title: {selectedJob.title}")
        print(f"\tJob description: {selectedJob.description}")
        print(f"\tEmployer: {selectedJob.employer}")
        print(f"\tJob location: {selectedJob.location}")
        print(f"\tSalary: {selectedJob.salary}")
        print(f"\tJob poster: {selectedJob.author}")

        if len(jobs) != 1:
            response = input("View another job details (Y/N)? ")
        else:
            input("No other jobs to view details of. Press enter to return to job list.")
            return

    if response.upper() == "N":
        settings.currentState = states.jobMenu  # Return to main menu with state mainMenu


def enterDeleteAJobMenu(dbCursor, dbConnection):
    print("Jobs you have posted:\n")
    userFullName = db.getUserFullName(dbCursor, settings.signedInUname)
    jobs = db.getJobsPostedByUser(dbCursor, userFullName)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i+1}. Job Title: {selectedJob.title}")
    else:
        input("You have not posted any jobs. You can only delete jobs you have posted.\nPress enter to return to previous menu.")
        settings.currentState = states.jobMenu
        return

    while True:
        job_index = input("Select a job 1 - " + str(len(jobs)) + " to delete: \n(Or press enter to return to previous menu)\n")
        if job_index == "":
            settings.currentState = states.jobMenu
            return
        try:
            int(job_index)
        except ValueError:
            print("Invalid input")
            continue
        if int(job_index) not in range(1, len(jobs) + 1):
            print("Invalid input")
            continue
        else:
            break

    Job = namedtuple('User', 'jobID title description employer location salary author')
    selectedJob = Job._make(jobs[int(job_index) - 1])

    # add notification to let job applicants that the job was deleted
    job_applicants = db.getJobApplicantsByTitle(dbCursor, selectedJob.title)
    if len(job_applicants) > 0:
        for applicant in job_applicants:
            db.insertNotification(dbCursor, "job_deleted", selectedJob.title, applicant[0])

    db.deleteJob(dbCursor, int(selectedJob.jobID))
    dbConnection.commit()
    print("Successfully deleted job")
    while True:
        choice = input("Delete another job? (Y/N)")
        if choice.upper() == "N":
            settings.currentState = states.jobMenu
            return
        elif choice.upper() == "Y":
            return
        else:
            print("Invalid input")


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
            settings.currentState = states.createJob          # returns to main() w/ currentState = createJob
        elif choice.upper() == "B":
            settings.currentState = states.deleteJob
            # settings.currentState = states.viewJobs           # returns to main() w/ currentState = viewJobs
        elif choice.upper() == "C":
            settings.currentState = states.viewJobs
            # settings.currentState = states.apply              # returns to main() w/ currentState = apply
        # elif choice.upper() == "D":
        #     settings.currentState = states.deleteJob          # returns to main() w/ currentState = deleteJob
        # elif choice.upper() == "E":
        #     settings.currentState = states.favoriteJob        # returns to main() w/ currentState = favoriteJob
        # elif choice.upper() == "F":
        #     settings.currentState = states.viewFavoriteJobs   # returns to main() w/ currentState = viewFavoriteJobs
        # elif choice.upper() == "G":
        #     settings.currentState = states.viewAppliedJobs    # returns to main() w/ currentState = viewAppliedJobs
        # elif choice.upper() == "H":
        #     settings.currentState = states.viewUnappliedJobs  # returns to main() w/ currentState = viewUnappliedJobs
        elif choice.upper() == "Z":
            settings.currentState = states.mainMenu           # returns to main() w/ currentState = mainMenu
        else:
            print(constants.INVALID_INPUT)


def enterViewJobsMenu(dbCursor, dbConnection):
    print("Choose filter:\n"
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
        if filterOption == 0:
            jobs = db.getAllJobs(dbCursor)
        elif filterOption == 1:
            jobs = db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)
        elif filterOption == 2:
            jobs = db.getAppliedJobs(dbCursor, settings.signedInUname)
        elif filterOption == 3:
            jobs = db.getUnappliedJobs(dbCursor, settings.signedInUname)

        if len(jobs) > 0:
            for i in range(len(jobs)):
                if len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, (jobs[i])[1])) > 0:  # if user has applied to this job
                    print(f"{i + 1}. {(jobs[i])[1]} (Applied)")
                else:
                    print(f"{i + 1}. {(jobs[i])[1]}")
        else:
            print("No jobs available under this filter, returning to previous menu.")
            return

        print("#. Choose one of the above jobs to view details")
        print("Z. Return to Previous Menu")

        while True:
            response = input("Input: ")
            if response.isdigit() and 1 <= int(response) <= len(jobs):
                selectedJob = jobs[int(response) - 1]
                viewJobDetails(dbCursor, selectedJob)
                break
            elif response.upper() == "Z":
                return
            else:
                print(constants.INVALID_INPUT)


def viewJobDetails(dbCursor, selectedJob):
    while True:
        print(f"Job title: {selectedJob[1]}")
        print(f"\tJob description: {selectedJob[2]}")
        print(f"\tEmployer: {selectedJob[3]}")
        print(f"\tJob location: {selectedJob[4]}")
        print(f"\tSalary: {selectedJob[5]}")
        print(f"\tJob poster: {selectedJob[6]}")
        print("A. Apply For Job")
        if any(selectedJob[0] in job for job in db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)):
            print("B. Unfavorite Job")
        else:
            print("B. Favorite Job")
        print("Z. Return to Previous Menu")
        while True:
            response2 = input("Input: ")
            if response2.upper() == "A":
                applyForJob(selectedJob)
                break
            elif response2.upper() == "B":
                if any(selectedJob[0] in job for job in db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)):
                    db.deleteFavoriteJob(dbCursor, settings.signedInUname, selectedJob[1])
                    print("Job unfavorited.")
                else:
                    db.insertFavoriteJob(dbCursor, settings.signedInUname, selectedJob[1])
                    print("Job favorited.")
                break
            elif response2.upper() == "Z":
                return
            else:
                print(constants.INVALID_INPUT)


def applyForJob(job):
    pass


# def applyForJob(dbCursor, dbConnection):
#     print("Jobs currently listed in the system:")
#     jobs = db.getAllJobs(dbCursor)
#     if len(jobs) > 0:
#         for i in range(0, len(jobs)):
#             # first create job object to select from
#             Job = namedtuple('User', 'jobID title description employer location salary author')
#             selectedJob = Job._make(jobs[i])
#             print(f"{i+1}. Job Title: {selectedJob.title}")
#     else:
#         input("No jobs have been posted\nPress enter to return to previous menu.")
#         settings.currentState = states.jobMenu
#         return
#
#     while True:
#         job_index = input("Select a job 1 - " + str(len(jobs)) + " to apply for: \n(Or press enter to return to previous menu)\n")
#         if job_index == "":
#             settings.currentState = states.jobMenu
#             return
#         try:
#             int(job_index)
#         except ValueError:
#             print("Invalid input")
#             continue
#         if int(job_index) not in range(1, len(jobs) + 1):
#             print("Invalid input")
#             continue
#         else:
#             break
#
#     Job = namedtuple('User', 'jobID title description employer location salary author')
#     selectedJob = Job._make(jobs[int(job_index) - 1])
#     job_title = selectedJob.title
#
#     # check if there are any existing applications to this job
#     applied = len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, job_title)) >= 1
#     if applied:
#         print("You have already applied for this job!\n")
#     else:
#         # PRINT APP MENU
#         grad = input("Please enter a graduation date (mm/dd/yyyy): ")
#         start = input("Please enter the earliest date you can start (mm/dd/yyyy): ")
#         credentials = input("Please briefly describe why you are fit for this job: ")
#         today = date.today()  # Get today's date
#         date_format = "%m/%d/%Y"
#         todayDate = today.strftime(date_format)  # Format date mm/dd/yyyy
#         currentDate = datetime.strptime(todayDate, date_format)  # Today's date as a string
#         db.insertUserJobApplication(dbCursor, settings.signedInUname, job_title, grad, start, credentials, currentDate)
#         dbConnection.commit()
#         print("Successfully applied for job")


def viewFavoriteJobs(dbCursor, dbConnection):
    print("Your favorited jobs:")
    jobs = db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i + 1}. Job Title: {selectedJob.title}")
    else:
        input("You currently have no favorited jobs.\nPress any key return to previous menu")
        settings.currentState = states.jobMenu
        return

    job_index = input("Select a job 1 - " + str(len(jobs)) + " to unfavorite: \n(Or press enter to return to previous menu)\n")
    if job_index == "":
        settings.currentState = states.jobMenu
        return
    try:
        int(job_index)
    except ValueError:
        print("Invalid input")
        return
    if int(job_index) not in range(1, len(jobs) + 1):
        print("Invalid input")
        return

    Job = namedtuple('User', 'jobID title description employer location salary author')
    selectedJob = Job._make(jobs[int(job_index) - 1])
    job_title = selectedJob.title

    db.deleteFavoriteJob(dbCursor, settings.signedInUname, job_title)
    dbConnection.commit()
    print("Job has been removed from favorites list.")


def viewAppliedJobs(dbCursor, dbConnection):
    print("Jobs you have applied for:")
    jobs = db.getAppliedJobs(dbCursor, settings.signedInUname)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i+1}. Job Title: {selectedJob.title}")

    else:
        print("You have not applied for any jobs yet")
    input("Press enter to return to previous menu:")
    settings.currentState = states.jobMenu


def viewUnappliedJobs(dbCursor, dbConnection):
    print("Jobs you have yet to apply for")
    jobs = db.getUnappliedJobs(dbCursor, settings.signedInUname)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i+1}. Job Title: {selectedJob.title}")
    else:
        print("None")
    input("Press enter to return to previous menu:")
    settings.currentState = states.jobMenu
