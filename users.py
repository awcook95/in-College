from collections import namedtuple

import dbfunctions as db
import settings
import states
import utils


def createUser(dbCursor, connection):
    # todo: possibly add exit option in case user wants to cancel account creation

    if db.getNumUsers(dbCursor) >= 10:  # checks if number of accounts in database is at max limit
        print("All permitted accounts have been created, please come back later")
        settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
        return

    uname = input("Enter your desired username: ")
    # added below if statement to return back to main menu if username is taken
    while db.getUserByName(dbCursor, uname):
        print("Sorry, that username has already been taken\n")
        uname = input("Enter your desired username: ")

    pword = input("Enter your desired password: ")
    while not utils.validatePassword(pword):
        print("Invalid password. Must be length 8-12 characters, contain one digit, one uppercase character, and one non-alphanumeric")
        pword = input("Enter your desired password: ")

    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")

    db.insertUser(dbCursor, uname, pword, fname, lname)
    db.insertUserSettings(dbCursor, uname, settings.emailNotif, settings.smsNotif, settings.targetAdvert, settings.language)
    db.insertProfilePage(dbCursor, uname, "", "", "")
    connection.commit()  # commits the new account and settings to the database (ensures account and settings are saved)

    settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut

    print("Account has been created")


def loginUser(dbCursor):
    # todo: possibly add exit option in case user wants to cancel account login

    uname = input("Enter your username: ")
    pword = input("Enter your password: ")

    while not db.tryLogin(dbCursor, uname, pword):
        print("Incorrect username / password, please try again\n")
        uname = input("Enter your username: ")
        pword = input("Enter your password: ")

    # read in user settings on login
    settings.signedInUname = uname # tracks the logged in user's username
    User = namedtuple('User', 'uname emailnotif smsnotif targetadvert languagepref')
    currentUser = User._make(db.getUserSettingsByName(dbCursor, settings.signedInUname))

    settings.emailNotif = currentUser.emailnotif
    settings.smsNotif = currentUser.smsnotif
    settings.targetAdvert = currentUser.targetadvert
    settings.language = currentUser.languagepref

    settings.signedIn = True                 # flags that a user is now signed in
    settings.currentState = states.mainMenu  # returns to incollege.py's main() w/ currentState = mainMenu

    print("You have successfully logged in.\n")


def logOutUser():
    print("Logging Out")
    settings.currentState = states.loggedOut
    settings.signedInUname = None
    settings.signedIn = False
    return True


def findUser(dbCursor, connection):
    while settings.currentState == states.userSearch:
        # Added the user prompt for searched person within this function
        print("Which search term do you want to find users by?")
        print("A. By Full Name")
        print("B. By Last Name")
        print("C. By University")
        print("D. By Major")
        print("Z. Return to the previous menu")
        response = input("Enter how you wish to search for a user: ")
        if response.upper() == 'A':
            name = input("Enter the name of a person you know: ").split(" ")

            # If the user enters an extra spaces at the end of first or last name they will be removed
            while("" in name):
                name.remove("")

            while len(name) != 2:
                print("Name must be in the form (firstname lastname)")
                name = input("Enter the name of a person you know: ").split(" ")

            first = name[0]
            last = name[1]

            result = db.getUserByFullName(dbCursor, first, last) # Find receiver for friend request
            break
        elif response.upper() == 'B':
            name = input("Enter the last name of the person you might know: ")
            users_found = utils.printUsersFoundLastName(dbCursor, name)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        first_name = (users_found[int(response) - 1])[2]            # parse first name from user object
                        last_name = (users_found[int(response) - 1])[3]             # parse last name from user object
                        result = db.getUserByFullName(dbCursor, first_name, last_name)
                        break
                    else:
                        print("Invalid input, try again.")
            break
        elif response.upper() == 'C':
            university = input("Enter the University of the person you might know goes to: ")
            users_found = utils.printUsersFoundParameter(dbCursor, university, 0)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        name = db.getUserByName(dbCursor, (users_found[int(response) - 1])[0])  # parses first and last name from user object
                        result = db.getUserByFullName(dbCursor, name[2], name[3])
                        break
                    else:
                        print("Invalid input, try again.")
            break
        elif response.upper() == 'D':
            major = input("Enter the major of the person you might know has: ")
            users_found = utils.printUsersFoundParameter(dbCursor, major, 1)
            if users_found is None:
                print("No users found under that criteria.")
                result = None
            else:
                while settings.currentState == states.userSearch:
                    response = input("Choose a person you might know: ")
                    if response.isdigit() and int(response) <= len(users_found):
                        name = db.getUserByName(dbCursor, (users_found[int(response) - 1])[0])  # parses first and last name from user object
                        result = db.getUserByFullName(dbCursor, name[2], name[3])
                        break
                    else:
                        print("Invalid input, try again.")
            break
        elif response.upper() == 'Z':
            if settings.signedIn:
                settings.currentState = states.mainMenu
            else:
                settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
            return False  # Didn't find user
        else:
            print("Invalid Option, enter the valid letter option")

    # If the desired user is found successfully, return their data and jump to appropriate menu
    if result is not None:
        User = namedtuple('User', 'uname pword firstname lastname')
        receiver = User._make(result)
        if settings.signedIn:
            friend_exists = db.checkUserFriendRelation(dbCursor, settings.signedInUname, receiver.uname)

            # If this person is already your friend,return
            if friend_exists:
                print(receiver.uname + " is already your friend!")
                settings.currentState = states.mainMenu   # returns to incollege.py's main() w/ currentState = mainMenu
                return True
        
        print("They are a part of the InCollege system!")
        if settings.signedIn:         # if a user is signed in
            if settings.signedInUname != receiver.uname: # Person you are requesting is not yourself
                response = input("Would you like to add them as a friend? Enter 'Y' for yes: ")
                request_exists = utils.checkExistingFriendRequest(dbCursor, settings.signedInUname, receiver.uname)
                
                if response.upper() == "Y":
                    # Send request if there is no pending request
                    if not request_exists:
                        print("Sending friend request! They will need to accept before they appear in your friends list!\n")
                        db.insertFriendRequest(dbCursor, settings.signedInUname, receiver.uname)
                        connection.commit()
                    else: 
                        print(receiver.uname + " has already been sent a request! They will show up in your friends list once they accept!")
            
            settings.currentState = states.mainMenu   # returns to incollege.py's main() w/ currentState = mainMenu
            return True
        else:                                         # else a user is not signed in
            settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
            return True
    else:
        while settings.currentState == states.userSearch:
            print("They are not yet a part of the InCollege system yet.")
            print("Options:\n")
            print("A. Search for another user")
            print("Z. Return to previous menu")
            response = input()
            if response.upper() == "A":
                break
            elif response.upper() == "Z":
                if settings.signedIn:
                    settings.currentState = states.mainMenu
                else:
                    settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
                return False  # Didn't find user
            else:
                print("Invalid input")


def postJob(dbCursor, dbConnection):
    if db.getNumJobs(dbCursor) >= 10:  # checks if number of jobs in database is at max limit
        print("All permitted jobs have been created, please come back later")
        settings.currentState = states.jobMenu
        return

    # Take input from user and create job in DB
    User = namedtuple('User', 'uname pword firstname lastname')
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
    dbConnection.commit()
    print("Job has been posted\n")
    settings.currentState = states.jobMenu  # returns to incollege.py's main() w/ currentState = jobMenu


def changeUserSettings(dbCursor, connection):
    while settings.currentState == states.modifyUserSettings:
        print("A. Email Notifications\n"
              "B. SMS Notifications\n"
              "C. Targeted Advertising\n"
              "Z. Return to previous menu")
        response = input("Select a setting to modify: ")
        if response.upper() == "A":
            option = input("Email Notifications - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.emailNotif = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "B":
            option = input("SMS Notifications - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.smsNotif = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "C":
            option = input("Targeted Advertising - enter 1 to turn on or enter 0 to turn off: ")
            if option == "1" or option == "0":
                settings.targetAdvert = option
                print("Setting changed; return to previous menu if logged in or create an account to save changes.")
            else:
                print("Invalid input, try again.")
        elif response.upper() == "Z":
            if settings.signedIn:
                db.updateUserSettings(dbCursor, settings.signedInUname, settings.emailNotif, settings.smsNotif, settings.targetAdvert)
                connection.commit()
                print("Settings successfully saved.")
            settings.currentState = states.importantLinks
        else:
            print("Invalid Option, enter the letter option you want and press enter")

def applyForJob(dbCursor, dbConnection):
    print("Jobs currently listed in the system:\n")
    jobs = db.getAllJobs(dbCursor)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i+1}. Job Title: {selectedJob.title}")
    else:
        input("No jobs have been posted\nPress enter to return to previous menu.")
        settings.currentState = states.jobMenu
        return
    
    global job_index
    while(True):
        job_index = input("Select a job 1 - " + str(len(jobs)) + " to apply for: \n(Or press enter to return to previous menu)\n")
        if job_index == "":
            settings.currentState = states.jobMenu
            return
        try:
            int(job_index)
        except ValueError:
            print("Invalid input")
            continue
        if int(job_index) not in range(1, int(str(len(jobs)))+1):
            print("Invalid input")
            continue
        else:
            break

    Job = namedtuple('User', 'jobID title description employer location salary author')
    selectedJob = Job._make(jobs[int(job_index)-1])
    job_title = selectedJob.title

    # check if there are any existing applications to this job
    applied = len(db.getUserJobApplicationByTitle(dbCursor, settings.signedInUname, job_title)) >= 1
    if applied:
        print("You have already applied for this job!\n")
    else:
        # PRINT APP MENU 
        grad = input("Please enter a graduation date (mm/dd/yyyy): ")
        start = input("Please enter the earliest date you can start (mm/dd/yyyy): ")
        credentials = input("Please brielfy describe why you are fit for this job: ")
        db.insertUserJobApplication(dbCursor, settings.signedInUname, job_title, grad, start, credentials)
        dbConnection.commit()
        print("Successfully applied for job")

def favoriteAJob(dbCursor, dbConnection):
    print("Jobs not yet favorited:\n")
    jobs = db.getJobsNotFavorited(dbCursor, settings.signedInUname)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])
            print(f"{i+1}. Job Title: {selectedJob.title}")
    else:
        input("None\nPress any key return to previous menu")
        settings.currentState = states.jobMenu
        return

    job_index = input("Select a job 1 - " + str(len(jobs)) + " to favorite: \n(Or press enter to return to previous menu)")
    if job_index == "":
        settings.currentState = states.jobMenu
        return
    try:
        int(job_index)
    except ValueError:
        print("Invalid input")
        return
    if int(job_index) not in range(1, int(str(len(jobs)))+1):
        print("Invalid input")
        return

    Job = namedtuple('User', 'jobID title description employer location salary author')
    selectedJob = Job._make(jobs[int(job_index)-1])
    job_title = selectedJob.title

    db.insertFavoriteJob(dbCursor, settings.signedInUname, job_title)
    dbConnection.commit()
    settings.currentState = states.jobMenu

