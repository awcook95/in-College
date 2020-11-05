from collections import namedtuple
from datetime import datetime
from datetime import date
import settings
import states
import users
import utils
import dbfunctions as db
import constants


def enterInitialMenu(dbCursor, dbConnection):
    while settings.currentState == states.loggedOut:  # change from currentState = loggedOut will result in return to incollege.py's main()
        # success story
        print(constants.SUCCESS_STORY)

        print("\nSelect Option:\n"
              "A. Log in with existing account\n"
              "B. Create new account\n"
              "C. Find someone you know\n"
              "D. Play success story video\n"
              "E. InCollege Useful Links\n"
              "F. InCollege Important Links\n"
              "Z. Quit")
        response = input("Input: ")
        if response.upper() == "A":
            settings.currentState = states.login          # returns to main() w/ currentState = login
        elif response.upper() == "B":
            settings.currentState = states.createAccount  # returns to main() w/ currentState = createAccount
        elif response.upper() == "C":
            settings.currentState = states.userSearch     # returns to main() w/ currentState = userSearch
        elif response.upper() == "D":
            print("Video is now playing")
        elif response.upper() == 'E':
            settings.currentState = states.usefulLinks
        elif response.upper() == "F":
            settings.currentState = states.importantLinks
        elif response.upper() == "Z":
            settings.currentState = states.quit           # returns to main() w/ currentState = quit
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterMainMenu(dbCursor, dbConnection):  # presents the user with an introductory menu if logged in
    while settings.currentState == states.mainMenu:  # change from currentState = mainMenu will result in return to incollege.py's main()

        # Check for any pending friend requests
        response = db.getUserFriendRequests(dbCursor, settings.signedInUname)

        messages = " (You have messages waiting for you)" if db.hasUnreadMessages(dbCursor, settings.signedInUname) else ""
        profileNotification = " (Don't forget to create a profile)" if db.profilePageExists(dbCursor, settings.signedInUname) == False else ""

        today = date.today() # Get today's date
        date_format = "%m/%d/%Y"
        todayDate = today.strftime(date_format) # Format date mm/dd/yyyy
        currentDate = datetime.strptime(todayDate, date_format) # Today's date as a string
        noJobNotification = ""

        if db.getJobAppliedDate(dbCursor, settings.signedInUname) == None:
            accountAge = datetime.strptime(db.getUserCreatedDate(dbCursor, settings.signedInUname), date_format) # Date account was created
            age = currentDate - accountAge # Length of time from account creation and today
            
            if age.days >= 7:
                noJobNotification = "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
        else:
            newestJob = datetime.strptime(db.getJobAppliedDate(dbCursor, settings.signedInUname), date_format) # Date of newest applied job
            newestJobAge = currentDate - newestJob # Length of time from newest applied job and today
            
            if newestJobAge.days >=7:
                noJobNotification = "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"

        print("Notifications:")

        # notifications for new students joined
        new_students_notifications = db.getNotificationsForUserByType(dbCursor, "new_student", settings.signedInUname)
        if len(new_students_notifications) > 0:
            for n in new_students_notifications:
                print(f"{n[2]} has joined InCollege.")
                db.deleteNotification(dbCursor, n[1], n[2], n[3])
                dbConnection.commit()

        print(noJobNotification)

        print("\nOptions:\n"
              "A. Jobs\n"
              "B. Find someone you know\n"
              "C. Learn a new skill\n"
              "D. InCollege Useful Links\n"
              "E. InCollege Important Links\n"
              "F. View Friends\n"
              f"G. Student Profile{profileNotification}\n"
              f"H. Message Center{messages}\n"
              "Z. Logout")

        if len(response) > 0:
            response = input("You have pending friend requests! Enter 'Y' to view them: ")
            if response.upper() == 'Y':
                utils.handleUserFriendRequests(dbCursor, dbConnection, settings.signedInUname)
                continue
        else:
            response = input("Input: ")
        if response.upper() == "A":
            settings.currentState = states.jobMenu
        elif response.upper() == "B":
            settings.currentState = states.userSearch   # returns to main() w/ currentState = userSearch
        elif response.upper() == "C":
            settings.currentState = states.selectSkill  # returns to main() w/ currentState = selectSkill
        elif response.upper() == "D":
            settings.currentState = states.usefulLinks
        elif response.upper() == "E":
            settings.currentState = states.importantLinks
        elif response.upper() == "F":
            settings.currentState = states.friendsMenu
        elif response.upper() == "G":
            settings.currentState = states.profilePage
        elif response.upper() == "H":
            settings.currentState = states.messageCenter
        elif response.upper() == "Z":
            users.logOutUser()  # logs user out: currentState = loggedOut; signedInUname = None; signedIn = False
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterSkillMenu(dbCursor, dbConnection):
    while settings.currentState == states.selectSkill:  # change from currentState = selectSkill will result in return to main()
        print("What skill would you like to learn?:\n"
              "A. Python\n"
              "B. How to make a resume\n"
              "C. Scrum\n"
              "D. Jira\n"
              "E. Software Engineering\n"
              "Z. None - return to menu")
        response = input()
        if response.upper() == "A":
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response.upper() == "B":
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response.upper() == "C":
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response.upper() == "D":
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response.upper() == "E":
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response.upper() == "Z":
            if not settings.signedIn:                     # if a user is not signed in
                settings.currentState = states.loggedOut  # returns to main() w/ currentState = loggedOut
            else:                                         # else a user is signed in
                settings.currentState = states.mainMenu   # returns to main() w/ currentState = mainMenu
            return False  # Don't learn skill
        else:
            print("Invalid Option, enter the number option you want and press enter")


def enterFriendsMenu(dbCursor, dbConnection):
    while settings.currentState == states.friendsMenu:
        print()
        friends = utils.printUserFriends(dbCursor, settings.signedInUname)
        if friends is None:
            print("No friends found. Add friends to view them here!")

        friend_requests = db.getUserFriendRequests(dbCursor, settings.signedInUname)
        if len(friend_requests) > 0:
            print("You have pending friend requests!")
        print("A. Delete a Friend")
        print("B. View Friend Requests")
        print("Z. Return to Previous Menu")
        response = input("Choose a friend to view their profile or enter another option: ")
        if response.isdigit() and int(response) <= len(friends):
            printProfilePage(dbCursor, (friends[int(response) - 1])[0])
        elif response.upper() == "A":
            if friends is None:
                print("No friends found.")
            else:
                response = input("Choose a friend you want to delete from your friends list or 'Z' to return to previous menu: ")
                # if response.isdigit() and int(response) <= len(friends):
                db.deleteUserFriend(dbCursor, settings.signedInUname, (friends[int(response) - 1])[0])
                db.deleteUserFriend(dbCursor, (friends[int(response) - 1])[0], settings.signedInUname)
                dbConnection.commit()
        elif response.upper() == "B":
            utils.handleUserFriendRequests(dbCursor, dbConnection, settings.signedInUname)
            dbConnection.commit()
        elif response.upper() == "Z":
            settings.currentState = states.mainMenu
        else:
            print("Invalid input, try again.")


def usefulLinksMenu(dbCursor, dbConnection):
    while settings.currentState == states.usefulLinks:
        print("Useful Links:")
        print("A. General")
        print("B. Browse InCollege")
        print("C. Business Solutions")
        print("D. Directories")
        print("Z. Return to Previous Menu")
        response = input()
        if response.upper() == 'A':
            settings.currentState = states.general
            return True
        if response.upper() == 'B':
            settings.currentState = states.browseInCollege
            return True
        if response.upper() == 'C':
            settings.currentState = states.businessSolutions
            return True
        if response.upper() == 'D':
            settings.currentState = states.directories
            return True
        if response.upper() == 'Z':
            if not settings.signedIn:
                settings.currentState = states.loggedOut
            else:
                settings.currentState = states.mainMenu
            return False  # No links chosen
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def generalMenu(dbCursor, dbConnection):
    while settings.currentState == states.general:
        print("Links:")
        print("A. Sign Up")
        print("B. Help Center")
        print("C. About")
        print("D. Press")
        print("E. Blog")
        print("F. Careers")
        print("G. Developers")
        print("Z. Return to Previous Menu")
        response = input()

        if response.upper() == 'A':
            if not settings.signedIn:
                settings.currentState = states.createAccount
            else:
                print("Already logged in as: " + settings.signedInUname + ", logout to create a new account!")
            return True
        elif response.upper() == 'B':
            print("We're here to help")
            return True
        elif response.upper() == 'C':
            print(constants.ABOUT)
            return True
        elif response.upper() == 'D':
            print("In College Pressroom: Stay on top of the latest news, updates, and reports")
            return True
        elif response.upper() == 'E':
            print("Under Construction")
            return True
        elif response.upper() == 'F':
            print("Under Construction")
            return True
        elif response.upper() == 'G':
            print("Under Construction")
            return True
        elif response.upper() == 'Z':
            settings.currentState = states.usefulLinks
            return False  # No links chosen
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def browseMenu(dbCursor, dbConnection):
    while settings.currentState == states.browseInCollege:
        print("Under Construction")
        settings.currentState = states.usefulLinks
        return True


def solutionsMenu(dbCursor, dbConnection):
    while settings.currentState == states.businessSolutions:
        print("Under Construction")
        settings.currentState = states.usefulLinks
        return True


def directoriesMenu(dbCursor, dbConnection):
    while settings.currentState == states.directories:
        print("Under Construction")
        settings.currentState = states.usefulLinks
        return True


def enterImportantLinksMenu(dbCursor, connection):
    while settings.currentState == states.importantLinks:
        print("\nInCollege Important Links:\n"
              "A. Copyright Notice\n"
              "B. About\n"
              "C. Accessibility\n"
              "D. User Agreement\n"
              "E. Privacy Policy\n"
              "F. Cookie Policy\n"
              "G. Copyright Policy\n"
              "H. Brand Policy\n"
              "I. Guest Controls\n"
              "J. Languages\n"
              "Z. Return to previous menu")
        response = input("Choose an option: ")
        if response.upper() == "A":
            print(constants.COPYRIGHT_NOTICE)
        elif response.upper() == "B":
            print(constants.ABOUT)
        elif response.upper() == "C":
            print(constants.ACCESSIBILITY)
        elif response.upper() == "D":
            print(constants.USER_AGREEMENT)
        elif response.upper() == "E":
            print(constants.PRIVACY_POLICY)
        elif response.upper() == "F":
            print(constants.COOKIE_POLICY)
        elif response.upper() == "G":
            print(constants.COPYRIGHT_POLICY)
        elif response.upper() == "H":
            print(constants.BRAND_POLICY)
        elif response.upper() == "I":
            settings.currentState = states.modifyUserSettings
        elif response.upper() == "J":
            print("Languages:\n"
                  "A. English\n"
                  "B. Spanish")
            option = input("Choose language preference: ")
            if option.upper() == "A":
                settings.language = "English"
            elif option.upper() == "B":
                settings.language = "Spanish"
            else:
                print("Invalid input, try again.")
                continue

            if settings.signedIn:
                db.updateUserLanguage(dbCursor, settings.signedInUname, settings.language)
                connection.commit()
                print("Language preference successfully saved.")
        elif response.upper() == "Z":
            if settings.signedIn:
                settings.currentState = states.mainMenu
            else:
                settings.currentState = states.loggedOut
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterProfilePageMenu(dbCursor, dbConnection):
    while settings.currentState == states.profilePage:
        major, university, about = printProfilePage(dbCursor, settings.signedInUname)
        print("A. Edit Profile Page")
        print("Z. Return to Previous Menu")
        response = input("Enter option: ")
        if response.upper() == 'A':
            settings.currentState = states.profilePageEdit
            while settings.currentState == states.profilePageEdit:
                print("Edit Profile")
                print("A. Major")
                print("B. University")
                print("C. About")
                print("D. Add Job")
                print("E. Education")
                print("Z. Return to Previous Menu")
                response = input("Enter option: ")
                if response.upper() == 'A':
                    major = input("Major: ").title()
                elif response.upper() == 'B':
                    university = input("University Name: ").title()
                elif response.upper() == 'C':
                    about = input("About: ")
                elif response.upper() == 'D':
                    if len(db.getProfileJobs(dbCursor, settings.signedInUname)) < constants.MAX_USER_PROFILE_JOBS:
                        print("Add a new job.")
                        title = input("Enter title: ")
                        employer = input("Enter employer: ")
                        date_start = input("Enter date started: ")
                        date_end = input("Enter date ended: ")
                        location = input("Enter location: ")
                        job_desc = input("Enter job description: ")
                        db.insertProfileJob(dbCursor, settings.signedInUname, title, employer, date_start, date_end, location, job_desc)
                    else:
                        print("Maximum number of jobs entered.")
                elif response.upper() == 'E':
                    print("Enter past education.")
                    university_name = input("Enter university name: ").title()
                    user_degree = input("Enter degree: ").title()
                    year_start = input("Enter year started: ")
                    year_end = input("Enter year ended: ")
                    db.insertProfileEducation(dbCursor, settings.signedInUname, university_name, user_degree, year_start, year_end)
                elif response.upper() == 'Z':
                    settings.currentState = states.profilePage
                    db.updateProfilePage(dbCursor, settings.signedInUname, major, university, about)
                    dbConnection.commit()
                else:
                    print("Invalid Option, enter the letter option you want and press enter")
                    continue
        elif response.upper() == 'Z':
            settings.currentState = states.mainMenu
            return False  # No links chosen
        else:
            print("Invalid Option, enter the letter option you want and press enter")
            continue


def printProfilePage(dbCursor, uname):
    name = db.getUserByName(dbCursor, uname)
    first = name[2]
    last = name[3]
    page = db.getProfilePage(dbCursor, uname)
    major = page[1]
    university = page[2]
    about = page[3]
    jobs = db.getProfileJobs(dbCursor, uname)
    education = db.getProfileEducation(dbCursor, uname)

    print(f"{first} {last}'s Profile Page")
    print(f"Major: {major}")
    print(f"University: {university}")
    print(f"About: \n{about}")
    if jobs is None:
        print("Career:")
    else:
        print("Career:")
        for job in jobs:
            title = job[2]
            employer = job[3]
            date_start = job[4]
            date_end = job[5]
            location = job[6]
            job_desc = job[7]
            print(title)
            print(f"\tEmployer: {employer}")
            print(f"\tDate: {date_start} - {date_end}")
            print(f"\tLocation: {location}")
            print(f"\tDescription: \n\t{job_desc}")
    if education is None:
        print("Education:")
    else:
        print("Education:")
        for i in education:
            university_name = i[2]
            user_degree = i[3]
            year_start = i[4]
            year_end = i[5]
            print(f"University: {university_name}")
            print(f"\tDegree: {user_degree}")
            print(f"\tYear: {year_start} - {year_end}")
    return major, university, about


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

    print("Notifications:")

    # notifications for new jobs posted
    new_jobs_notifications = db.getNotificationsForUserByType(dbCursor, "new_job", settings.signedInUname)
    if len(new_jobs_notifications) > 0:
        for n in new_jobs_notifications:
            print(f"A new job '{n[2]}' has been posted.")
            db.deleteNotification(dbCursor, n[1], n[2], n[3])
            dbConnection.commit()
    else:
        print("No current notifications.")

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


def messageCenterMenu(dbCursor, dbConnection):
    print("Select a messaging option:\n"
          "A. Inbox\n"
          "B. Send Message\n"
          "Z. Return to Previous Menu")
    choice = input("Input: ")

    if choice.upper() == "A":
        settings.currentState = states.inbox        # returns to main() w/ currentState = inbox
    elif choice.upper() == "B":
        settings.currentState = states.sendMessage  # returns to main() w/ currentState = sendMessage
    elif choice.upper() == "Z":
        settings.currentState = states.mainMenu     # returns to main() w/ currentState = mainMenu


def inboxMenu(dbCursor, dbConnection):
    # Display list of messages
    messages = db.getMessageByReceiver(dbCursor, settings.signedInUname)
    if len(messages) == 0:
        print("You have no messages.")
        settings.currentState = states.messageCenter
    else:
        Message = namedtuple('User', 'message_id sender_uname receiver_uname body read')
        for i in range(0, len(messages)):
            # first create message object to select from
            selectedMessage = Message._make(messages[i])
            if selectedMessage.read == 0:
                print(f"{i+1}. {selectedMessage.sender_uname} (Unread)")
            else:
                print(f"{i+1}. {selectedMessage.sender_uname} ")

        print("\n")
        if len(messages) > 1:
            choice = input("Select a message 1 - " + str(len(messages)) + " to read: \n(Or press enter to return to previous menu)\n")
        else:
            choice = input("Enter '1' to read this message\n(Or press enter to return to previous menu)\n")
        if choice == "":
            settings.currentState = states.messageCenter  # returns to main() w/ currentState = messageCenter
            return
        try:
            int(choice)
        except ValueError:
            print("Invalid input\n")
            return
        if int(choice) not in range(1, len(messages) + 1):
            print("Invalid input\n")
            return

        selectedMessage = Message._make(messages[int(choice) - 1])
        print(f"{selectedMessage.body}\n")  # Print Message
        db.updateMessageAsRead(dbCursor, selectedMessage.message_id)  # Mark message as read
        dbConnection.commit()

        response = input(f"Would you like to send a reply to {selectedMessage.sender_uname}? (Y/N): ")
        if response.upper() == 'Y':
            reply = input(f"Enter message to {selectedMessage.sender_uname}: ")
            db.insertMessage(dbCursor, settings.signedInUname, selectedMessage.sender_uname, reply)  # Add new message
            dbConnection.commit()
            print("Message Sent")

        option = input(f"Would you like to delete {selectedMessage.sender_uname}'s message? (Y/N): ")
        if option.upper() == 'Y':
            db.deleteMessage(dbCursor, selectedMessage.message_id)  # Delete Message
            dbConnection.commit()
            print("Message Deleted")


def sendMessageMenu(dbCursor, dbConnection):
    friends = db.getUserFriends(dbCursor, settings.signedInUname)
    allUsers = db.getAllOtherUsers(dbCursor, settings.signedInUname)
    choice = "A"
    users = friends
    while True:
        if choice.upper() == "A":
            print("Your friends:")
        elif choice.upper() == "B":
            print("All InCollege users:")
        if len(users) > 0:
            for i in range(0, len(users)):
                user = namedtuple('user', 'uname pword firstname lastname plus_member')
                selectedUser = user._make(users[i])
                print(f"{i + 1}. {selectedUser.firstname} {selectedUser.lastname}")
        else:
            if choice.upper() == "A":
                print("None, go add some friends!:\n")
            elif choice.upper() == "B":
                print("No InCollege users found.\n")

        choice = input("{selectionRange}"
            "A. View my friends\n"
            "B. View all InCollege users\n"
            "Z. Return to previous menu\n"
            "input: ".format(selectionRange="\nSelect a user 1 - " + str(len(users)) + " to message: \n\n" if len(users) > 1 else "Enter '1' to message this user\n\n" if len(users) == 1 else "")
        )

        if choice.upper() == "A":
            users = friends
            continue
        elif choice.upper() == "B":
            users = allUsers
            continue
        elif choice.upper() == "Z":
            settings.currentState = states.messageCenter
            return
        try:
            int(choice)
        except ValueError:
            print("Invalid input")
            continue

        if len(users) == 0:
            print("Invalid input")
            continue

        if int(choice) not in range(1, len(users) + 1):
            print(f"Input must be 1 through {len(users) + 1}")
            continue

        user = namedtuple('user', 'uname pword firstname lastname plus_member')
        selectedUser = user._make(users[int(choice) - 1])

        if not db.checkUserFriendRelation(dbCursor, settings.signedInUname, selectedUser.uname) and not db.userIsPlusMember(dbCursor, settings.signedInUname):
            print("I'm sorry, you are not friends with that person -- Only InCollege Plus members may send messages to non-friends.")
            continue

        message = input(f"Enter your message you would like to send to {selectedUser.uname}: ")
        db.insertMessage(dbCursor, settings.signedInUname, selectedUser.uname, message)
        dbConnection.commit()
        print("Message sent")
