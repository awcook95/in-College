import settings
import states
import users
import dbfunctions as db


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
        print()
        print("Useful Links:")
        print("E. General")
        print("F. Browse InCollege")
        print("G. Business Solutions")
        print("H. Directories")
        print("I. InCollege Important Links")
        print("Z. Quit")
        response = input()
        if response.upper() == "A":
            settings.currentState = states.login          # returns to incollege.py's main() w/ currentState = login
        elif response.upper() == "B":
            settings.currentState = states.createAccount  # returns to incollege.py's main() w/ currentState = createAccount
        elif response.upper() == "C":
            settings.currentState = states.userSearch     # returns to incollege.py's main() w/ currentState = userSearch
        elif response.upper() == "D":
            print("Video is now playing")
        elif response.upper() == 'E':
            settings.currentState = states.general
        elif response.upper() == 'F':
            settings.currentState = states.browseInCollege
        elif response.upper() == 'G':
            settings.currentState = states.businessSolutions
        elif response.upper() == 'H':
            settings.currentState = states.directories
        elif response.upper() == "I":
            settings.currentState = states.importantLinks
        elif response.upper() == "Z":
            settings.currentState = states.quit           # returns to incollege.py's main() w/ currentState = quit
        else:
            print("Invalid Option, enter the letter option you want and press enter")


def enterMainMenu():  # presents the user with an introductory menu
    while settings.currentState == states.mainMenu:  # change from currentState = mainMenu will result in return to incollege.py's main()
        print("Options:\n"
              "A. Search for a job/internship\n"
              "B. Post a job\n"
              "C. Find someone you know\n"
              "D. Learn a new skill\n")
        print()
        print("Useful Links:")
        print("E. General")
        print("F. Browse InCollege")
        print("G. Business Solutions")
        print("H. Directories")
        print("I. InCollege Important Links")
        print("Z. Logout")

        response = input()
        if response.upper() == "A":
            print("Under Construction")
        elif response.upper() == "B":
            settings.currentState = states.createJob    # returns to incollege.py's main() w/ currentState = createJob
        elif response.upper() == "C":
            settings.currentState = states.userSearch   # returns to incollege.py's main() w/ currentState = userSearch
        elif response.upper() == "D":
            settings.currentState = states.selectSkill  # returns to incollege.py's main() w/ currentState = selectSkill
        elif response.upper() == 'E':
            settings.currentState = states.general
        elif response.upper() == 'F':
            settings.currentState = states.browseInCollege
        elif response.upper() == 'G':
            settings.currentState = states.businessSolutions
        elif response.upper() == 'H':
            settings.currentState = states.directories
        elif response.upper() == "I":
            settings.currentState = states.importantLinks
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

            
def generalMenu():
    while settings.currentState == states.general:
        print("Links:")
        print("1. Sign Up")
        print("2. Help Center")
        print("3. About")
        print("4. Press")
        print("5. Blog")
        print("6. Careers")
        print("7. Developers")
        print("8. Return to Previous Page")
        response = input()
        
        if response == '1':
            settings.currentState = states.createAccount
            return True
        elif response == '2':
            print("We're here to help")
            return True
        elif response == '3':
            print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
            return True
        elif response == '4':
            print("In College Pressroom: Stay on top of the latest news, updates, and reports")
            return True
        elif response == '5':
            print("Under Construction")
            return True
        elif response == '6':
            print("Under Construction")
            return True
        elif response == '7':
            print("Under Construction")
            return True
        elif response == '8':
            if not settings.signedIn:
                settings.currentState = states.loggedOut
            else:
                settings.currentState = states.mainMenu
            return False  # No links chosen
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue

            
def browseMenu():
    while settings.currentState == states.browseInCollege:
        print("Under Construction")
        if not settings.signedIn:
            settings.currentState = states.loggedOut
            return True
        else:
            settings.currentState = states.mainMenu
            return True
        
        
def solutionsMenu():
    while settings.currentState == states.businessSolutions:
        print("Under Construction")
        if not settings.signedIn:
            settings.currentState = states.loggedOut
            return True
        else:
            settings.currentState = states.mainMenu
            return True
    
    
def directoriesMenu():
    while settings.currentState == states.directories:
        print("Under Construction")
        if not settings.signedIn:
            settings.currentState = states.loggedOut
            return True
        else:
            settings.currentState = states.mainMenu
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
