from collections import namedtuple
from datetime import datetime
from datetime import date
import profiles
import settings
import states
import users
import utils
import database as db
import constants


def enterInitialMenu(dbCursor, dbConnection):
    while settings.currentState == states.loggedOut:  # change from currentState = loggedOut will result in return to main()
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
    while settings.currentState == states.mainMenu:  # change from currentState = mainMenu will result in return to main()

        # Check for any pending friend requests
        response = db.getUserFriendRequests(dbCursor, settings.signedInUname)

        messages = " (You have messages waiting for you)" if db.hasUnreadMessages(dbCursor, settings.signedInUname) else ""
        profileNotification = " (Don't forget to create a profile)" if db.profilePageExists(dbCursor, settings.signedInUname) is False else ""

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
        response = input("Input: ")
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
            profiles.printProfilePage(dbCursor, (friends[int(response) - 1])[0])
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
        response = input("Input: ")
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
        response = input("Input: ")

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
