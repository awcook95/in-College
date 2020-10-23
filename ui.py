from collections import namedtuple
import settings
import states
import users
import utils
import dbfunctions as db
import os           # These are used to clear the console when switching between menus
import subprocess   #

def clear(): # Clear console to print menu on blank page
    print("\n" * 120)

def enterInitialMenu():
    while settings.currentState == states.loggedOut:  # change from currentState = loggedOut will result in return to incollege.py's main()
        # success story
        print("\nNathan Cooper had always dreamed about getting a software engineering job after graduating from college.\n"
              "However, with no work history and no connections, he feared that finding a company to hire him after graduation\n"
              "would be difficult. After using inCollege, Nathan was able to connect with other students in the same major to\n"
              "discuss school, jobs, salaries, offers, and projects. He was also able to learn new skills that would increase\n"
              "his experience and improve the look of his resume.\n")

        print("Select Option:")
        print("A. Log in with existing account")
        print("B. Create new account")
        print("C. Find someone you know")
        print("D. Play success story video")
        print("E. InCollege Useful Links")
        print("F. InCollege Important Links")
        print("Z. Quit")
        response = input("Input: ")
        if response.upper() == "A":
            settings.currentState = states.login          # returns to incollege.py's main() w/ currentState = login
        elif response.upper() == "B":
            settings.currentState = states.createAccount  # returns to incollege.py's main() w/ currentState = createAccount
        elif response.upper() == "C":
            settings.currentState = states.userSearch     # returns to incollege.py's main() w/ currentState = userSearch
        elif response.upper() == "D":
            print("Video is now playing")
        elif response.upper() == 'E':
            settings.currentState = states.usefulLinks
        elif response.upper() == "F":
            settings.currentState = states.importantLinks
        elif response.upper() == "Z":
            settings.currentState = states.quit           # returns to incollege.py's main() w/ currentState = quit
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterMainMenu(dbCursor, dbConnection):  # presents the user with an introductory menu if logged in
    while settings.currentState == states.mainMenu:  # change from currentState = mainMenu will result in return to incollege.py's main()
        
        # Check for any pending friend requests
        response = db.getUserFriendRequests(dbCursor, settings.signedInUname)

        print("Options:\n"
              "A. Search for a job/internship\n"
              "B. Find someone you know\n"
              "C. Learn a new skill\n"
              "D. InCollege Useful Links\n"
              "E. InCollege Important Links\n"
              "F. View Friends\n"
              "G. Student Profile\n"
              "Z. Logout\n")

        if len(response) > 0:
            response = input("You have pending friend requests! Enter 'Y' to view them\nInput: ")
            if(response.upper() == 'Y'):
                utils.handleUserFriendRequests(dbCursor, dbConnection, settings.signedInUname)
                continue
        else:
            response = input("\nInput: ")
        if response.upper() == "A":
            enterJobMenu()
        elif response.upper() == "B":
            settings.currentState = states.userSearch   # returns to incollege.py's main() w/ currentState = userSearch
        elif response.upper() == "C":
            settings.currentState = states.selectSkill  # returns to incollege.py's main() w/ currentState = selectSkill
        elif response.upper() == "D":
            settings.currentState = states.usefulLinks
        elif response.upper() == "E":
            settings.currentState = states.importantLinks
        elif response.upper() == "F":
            settings.currentState = states.friendsMenu
        elif response.upper() == "G":
            settings.currentState = states.profilePage
        elif response.upper() == "Z":
            users.logOutUser()  # logs user out: currentState = loggedOut; signedInUname = None; signedIn = False
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterSkillMenu():
    # Skills menu will display under construction menus and return status
    while settings.currentState == states.selectSkill:  # change from currentState = selectSkill will result in return to incollege.py's main()
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
                settings.currentState = states.loggedOut  # returns to incollege.py's main() w/ currentState = loggedOut
            else:                                         # else a user is signed in
                settings.currentState = states.mainMenu   # returns to incollege.py's main() w/ currentState = mainMenu
            return False  # Don't learn skill
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


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

         
def usefulLinksMenu():
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
            continue
        
        
def generalMenu():
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
            print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
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
            continue

            
def browseMenu():
    while settings.currentState == states.browseInCollege:
        print("Under Construction")
        settings.currentState = states.usefulLinks
        return True
        
        
def solutionsMenu():
    while settings.currentState == states.businessSolutions:
        print("Under Construction")
        settings.currentState = states.usefulLinks
        return True
    
    
def directoriesMenu():
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
            print("Copyright © InCollege Corporation. All rights reserved.")
        elif response.upper() == "B":
            print("InCollege: Welcome to InCollege, the world's largest college student"
                  " network with many users in many countries and territories worldwide")
        elif response.upper() == "C":
            print("Accessibility:\n"
                  "Our goal at InCollege is to make our services accessible to as many college students as possible\n"
                  "in order to help them achieve their goals for the future.")
        elif response.upper() == "D":
            print("User Agreement:\n"
                  "You agree that by creating an InCollege account, you are agreeing to enter into a legally binding\n"
                  "contract with InCollege. If you do not agree to this, do not create an InCollege account.")
        elif response.upper() == "E":
            print("Privacy Policy:\n"
                  "To create an account, you need to provide your name and a password. Optionally, you may also provide\n"
                  "an email and/or phone number. How we use your data depends on which services of ours you decide to\n"
                  "Email and phone notifications as well as targeted advertising help us to enhance your experience\n"
                  "with InCollege; these options are able to be turned on or off in your account settings.")
        elif response.upper() == "F":
            print("Cookie Policy:\n"
                  "InCollege uses cookies to collect and use data for the purposes defined in our Privacy Policy.\n"
                  "By using our services, you are agreeing to the use of cookies for these purposes.")
        elif response.upper() == "G":
            print("Copyright Policy:\n"
                  "InCollege respects the intellectual property rights of others and desires to offer a platform\n"
                  "which contains no content that violates those rights.")
        elif response.upper() == "H":
            print("Brand Policy:\n"
                  "InCollege permits its members, third party developers, partners and the media to use its name,\n"
                  "logos, screenshots and other brand features only in limited circumstances.")
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
                print("A. Major")  # major
                print("B. University")  # uni name
                print("C. About")  # paragraph of info about student
                print("D. Add Job: ")  # experience of jobs if any, dont show if none, up to 3, title, employer, date started, date ended, location, description of what did
                print("E. Education: ")  # 1 or more lines about education, school name, degree, year start, year end date
                print("Z. Return to Previous Menu")
                response = input("Enter option: ")
                if response.upper() == 'A':
                    major = input("Major: ").title()
                elif response.upper() == 'B':
                    university = input("University Name: ").title()
                elif response.upper() == 'C':
                    about = input("About: ")
                elif response.upper() == 'D':
                    if len(db.getProfileJobs(dbCursor, settings.signedInUname)) < 3:
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

    print(f"{first} {last}'s Profile Page")  # title
    print(f"Major: {major}")  # major
    print(f"University: {university}")  # uni name
    print(f"About: \n{about}")  # paragraph of info about student
    if jobs is None:
        print("Career:")  # experience of jobs if any, dont show if none, up to 3, title, employer, date started, date ended, location, description of what did
    else:
        print("Career:")
        for i in jobs:
            title = i[2]
            employer = i[3]
            date_start = i[4]
            date_end = i[5]
            location = i[6]
            job_desc = i[7]
            print(title)
            print(f"\tEmployer: {employer}")
            print(f"\tDate: {date_start} - {date_end}")
            print(f"\tLocation: {location}")
            print(f"\tDescription: \n\t{job_desc}")
    if education is None:
        print("Education:")  # 1 or more lines about education, school name, degree, year start, year end date
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
            print(f"{i+1}. Job Title: {selectedJob.title}")

    response = input("View Job details (Y/N)? ")
    # print full job details
    while response.upper() == "Y":
        Job = namedtuple('User', 'jobID title description employer location salary author')
        if len(jobs) != 1: 
            job_id = input("Which job 1 - " + str(len(jobs)) + " would you like to view? ")
            selectedJob = Job._make(jobs[int(job_id) - 1])
        else:
            selectedJob = Job._make(jobs[0])

        print(f"Job title: {selectedJob.title}")
        print(f"\tJob description: {selectedJob.description}")
        print(f"\tEmployer: {selectedJob.employer}")
        print(f"\tJob location: {selectedJob.location}")
        print(f"\tSalary: {selectedJob.salary}")
        print(f"\tJob poster: {selectedJob.author}")

        response = input("View another job details (Y/N)? ")

    if response.upper() == "N":
        settings.currentState = states.jobMenu # Return to main menu with state mainMenu

def enterDeleteAJobMenu(dbCursor, dbConnection):
    print("Jobs you have posted:\n")
    User = namedtuple('User', 'uname pword firstname lastname')
    currentUser = User._make(db.getUserByName(dbCursor, settings.signedInUname))

    first = currentUser.firstname
    last = currentUser.lastname
    author = first + " " + last
    jobs = db.getJobsByAuthor(dbCursor, author)
    if len(jobs) > 0:
        for i in range(0, len(jobs)):
            # first create job object to select from
            Job = namedtuple('User', 'jobID title description employer location salary author')
            selectedJob = Job._make(jobs[i])

            print(f"{i+1}. Job Title: {selectedJob.title}")
            print(f"\tJob Description: {selectedJob.description}")
            print(f"\tEmployer Name: {selectedJob.employer}")
            print(f"\tJob Location: {selectedJob.location}")
            print(f"\tSalary: ${selectedJob.salary}")
            print(f"\tJob Poster: {selectedJob.author}\n")
            response = input("Delete this job (Y/N)? ")
            # could make this into a while loop that contiually asks for input
            if response.upper() == "Y":
                db.deleteJob(dbCursor, selectedJob.jobID)
                dbConnection.commit()
            elif response.upper() == "N":
                continue
        clear()
        settings.currentState = states.jobMenu
    else: 
        print("You have not posted any jobs! You can only delete jobs you have posted. \n")
        settings.currentState = states.jobMenu

def enterJobMenu():
    print("Select a job function: \n")
    choice = input("A. Post a job\n"  
                "B. View posted jobs\n"
                "C. Apply for a job\n"
                "D. Delete a job\n"
                "E. Favorite a job\n"
                "F. View favorited jobs\n"
                "G. View jobs applied for\n"
                "H. View jobs not applied for\n"
                "Z. Return to main menu\n"

                "input: ")
    if choice.upper() == "A":
        settings.currentState = states.createJob    # returns to incollege.py's main() w/ currentState = createJob
    elif choice.upper() == "B":
        settings.currentState = states.viewJobs     # returns to incollege.py's main() w/ currentState = viewJobs
    elif choice.upper() == "C":
        settings.currentState = states.apply     # returns to incollege.py's main() w/ currentState = viewJobs
    elif choice.upper() == "D":
        settings.currentState = states.deleteJob # returns to incollege.py's main() w/ currentState = deleteJob
    elif choice.upper() == "E":
        settings.currentState = states.favoriteJob # returns to incollege.py's main() w/ currentState = favoriteJob
    elif choice.upper() == "F":
        settings.currentState = states.viewFavoriteJobs # returns to incollege.py's main() w/ currentState = viewFavoriteJobs
    elif choice.upper() == "G":
        settings.currentState = states.viewAppliedJobs # returns to incollege.py's main() w/ currentState = viewAppliedJobs
    elif choice.upper() == "H":
        settings.currentState = states.viewUnappliedJobs # returns to incollege.py's main() w/ currentState = viewUnappliedJobs
    elif choice.upper() == "Z":
        settings.currentState = states.mainMenu

def viewFavoriteJobs(dbCursor, dbConnection):
    print("Your favorited jobs:\n")
    jobs = db.getFavoriteJobsByUser(dbCursor, settings.signedInUname)
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

    job_index = input("Select a job 1 - " + str(len(jobs)) + " to unfavorite: \n(Or press enter to return to previous menu)\n")
    if job_index == "":
        settings.currentState = states.jobMenu
        return
    Job = namedtuple('User', 'jobID title description employer location salary author')
    selectedJob = Job._make(jobs[int(job_index)-1])
    job_title = selectedJob.title

    db.deleteFavoriteJob(dbCursor, settings.signedInUname, job_title)
    dbConnection.commit()
    settings.currentState = states.jobMenu

def viewAppliedJobs(dbCursor, dbConnection):
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