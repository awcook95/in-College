import constants
import database as db
import notifications
import profiles
import settings
import states
import users
import utils


def enterInitialMenu(dbCursor, dbConnection):
    print(constants.SUCCESS_STORY)  # student success story

    print("\nSelect Option:\n"
          "A. Log in with existing account\n"
          "B. Create new account\n"
          "C. Find someone you know\n"
          "D. Play success story video\n"
          "E. InCollege Useful Links\n"
          "F. InCollege Important Links\n"
          "G. Training\n"
          "Z. Quit")

    while settings.currentState == states.loggedOut:  # change from currentState = loggedOut will result in return to main()
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
        elif response.upper() == "G":
            settings.currentState = states.training       # returns to main() w/ currentState = training
        elif response.upper() == "Z":
            settings.currentState = states.quit           # returns to main() w/ currentState = quit
        else:
            print(constants.INVALID_INPUT)


def enterMainMenu(dbCursor, dbConnection):  # presents the user with an introductory menu if logged in
    # Check for any pending friend requests
    friendRequests = db.getUserFriendRequests(dbCursor, settings.signedInUname)

    messages = " (You have messages waiting for you)" if db.hasUnreadMessages(dbCursor, settings.signedInUname) else ""
    profileNotification = " (Don't forget to create a profile)" if db.profilePageExists(dbCursor, settings.signedInUname) is False else ""

    notifications.printMainMenuNotifications(dbCursor, dbConnection)

    print("\nOptions:\n"
          "A. Jobs\n"
          "B. Find someone you know\n"
          "C. Learn a new skill\n"
          "D. InCollege Useful Links\n"
          "E. InCollege Important Links\n"
          "F. View Friends\n"
          f"G. Student Profile{profileNotification}\n"
          f"H. Message Center{messages}\n"
          "I. InCollege Learning\n"
          "Z. Logout")
    if len(friendRequests) > 0:
        print("You have pending friend requests! Enter 'Y' to view them.")

    while settings.currentState == states.mainMenu:  # change from currentState = mainMenu will result in return to main()
        response = input("Input: ")
        if len(friendRequests) > 0:
            if response.upper() == 'Y':
                utils.handleUserFriendRequests(dbCursor, dbConnection, settings.signedInUname)
                break
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
        elif response.upper() == "I":
            settings.currentState = states.learning
        elif response.upper() == "Z":
            users.logOutUser()  # logs user out: currentState = loggedOut; signedInUname = None; signedIn = False
        else:
            print(constants.INVALID_INPUT)


def enterSkillMenu(dbCursor, dbConnection):
    print("\nWhat skill would you like to learn?:\n"
          "A. Python\n"
          "B. How to make a resume\n"
          "C. Scrum\n"
          "D. Jira\n"
          "E. Software Engineering\n"
          "Z. None - return to menu")

    while settings.currentState == states.selectSkill:  # change from currentState = selectSkill will result in return to main()
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
            print(constants.INVALID_INPUT)


def enterFriendsMenu(dbCursor, dbConnection):
    while settings.currentState == states.friendsMenu:
        print()
        friends = utils.printUserFriends(dbCursor, settings.signedInUname)
        if friends is None:
            print("No friends found. Add friends to view them here!")

        friend_requests = db.getUserFriendRequests(dbCursor, settings.signedInUname)
        if len(friend_requests) > 0:
            print("You have pending friend requests!")
        print("#. Choose a friend to view their profile")
        print("A. Delete a Friend")
        print("B. View Friend Requests")
        print("Z. Return to Previous Menu")
        response = input("Input: ")
        if response.isdigit() and int(response) <= len(friends):
            profiles.printProfilePage(dbCursor, (friends[int(response) - 1])[0])
        elif response.upper() == "A":
            if friends is None:
                print("No friends found.")
            else:
                while True:
                    response = input("Choose a friend you want to delete from your friends list or 'Z' to return: ")
                    if response.isdigit() and 1 <= int(response) <= len(friends):
                        db.deleteUserFriend(dbCursor, settings.signedInUname, (friends[int(response) - 1])[0])
                        db.deleteUserFriend(dbCursor, (friends[int(response) - 1])[0], settings.signedInUname)
                        dbConnection.commit()
                        print(f"{(friends[int(response) - 1])[0]} has been deleted.")
                        break
                    elif response.upper() == "Z":
                        break
                    else:
                        print(constants.INVALID_INPUT)
        elif response.upper() == "B":
            utils.handleUserFriendRequests(dbCursor, dbConnection, settings.signedInUname)
            dbConnection.commit()
        elif response.upper() == "Z":
            settings.currentState = states.mainMenu
        else:
            print(constants.INVALID_INPUT)


def usefulLinksMenu(dbCursor, dbConnection):
    print("\nUseful Links:")
    print("A. General")
    print("B. Browse InCollege")
    print("C. Business Solutions")
    print("D. Directories")
    print("Z. Return to Previous Menu")

    while settings.currentState == states.usefulLinks:
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
            print(constants.INVALID_INPUT)


def generalMenu(dbCursor, dbConnection):
    print("\nLinks:")
    print("A. Sign Up")
    print("B. Help Center")
    print("C. About")
    print("D. Press")
    print("E. Blog")
    print("F. Careers")
    print("G. Developers")
    print("Z. Return to Previous Menu")

    while settings.currentState == states.general:
        response = input("Input: ")
        if response.upper() == 'A':
            if not settings.signedIn:
                settings.currentState = states.createAccount
            else:
                print(f"Already logged in as: {settings.signedInUname}, logout to create a new account!")
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
            print(constants.INVALID_INPUT)


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

    while settings.currentState == states.importantLinks:
        response = input("Input: ")
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
            print("\nLanguages:\n"
                  "A. English\n"
                  "B. Spanish")
            option = input("Choose language preference: ")
            while True:
                if option.upper() == "A":
                    settings.language = "English"
                    break
                elif option.upper() == "B":
                    settings.language = "Spanish"
                    break
                else:
                    print(constants.INVALID_INPUT)
                    continue

            if settings.signedIn:
                db.updateUserLanguage(dbCursor, settings.signedInUname, settings.language)
                connection.commit()
                print("Language preference successfully saved.")
            else:
                print("Sign in or create an account to be able to save your language preference.")

            break
        elif response.upper() == "Z":
            if settings.signedIn:
                settings.currentState = states.mainMenu
            else:
                settings.currentState = states.loggedOut
        else:
            print(constants.INVALID_INPUT)
