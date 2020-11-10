from collections import namedtuple
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


def enterJobMenu(dbCursor, dbConnection):  # todo: make this menu more concise
    appliedJobs = len(db.getAppliedJobs(dbCursor, settings.signedInUname))
    if db.getAppliedJobs(dbCursor, settings.signedInUname):
        if appliedJobs == 1:
            numJobNotification = " (You have currently applied for 1 job)"
        else:
            numJobNotification = " (You have currently applied for {} jobs)".format(appliedJobs)
    else:
        numJobNotification = " (You have currently applied for 0 jobs)"

    notifications.printJobNotifications(dbCursor, dbConnection)

    print("\nSelect a job function:\n"
          "A. Post Job\n"
          "B. View Posted Jobs\n"
          "C. Apply for Job\n"
          "D. Delete Job\n"
          "E. Favorite Job\n"
          "F. View Favorite Jobs\n"
          f"G. View Jobs Applied To{numJobNotification}\n"
          "H. View Jobs Not Applied To\n"
          "Z. Return to Previous Menu")
    choice = input("Input: ")
    if choice.upper() == "A":
        settings.currentState = states.createJob          # returns to main() w/ currentState = createJob
    elif choice.upper() == "B":
        settings.currentState = states.viewJobs           # returns to main() w/ currentState = viewJobs
    elif choice.upper() == "C":
        settings.currentState = states.apply              # returns to main() w/ currentState = apply
    elif choice.upper() == "D":
        settings.currentState = states.deleteJob          # returns to main() w/ currentState = deleteJob
    elif choice.upper() == "E":
        settings.currentState = states.favoriteJob        # returns to main() w/ currentState = favoriteJob
    elif choice.upper() == "F":
        settings.currentState = states.viewFavoriteJobs   # returns to main() w/ currentState = viewFavoriteJobs
    elif choice.upper() == "G":
        settings.currentState = states.viewAppliedJobs    # returns to main() w/ currentState = viewAppliedJobs
    elif choice.upper() == "H":
        settings.currentState = states.viewUnappliedJobs  # returns to main() w/ currentState = viewUnappliedJobs
    elif choice.upper() == "Z":
        settings.currentState = states.mainMenu           # returns to main() w/ currentState = mainMenu


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
