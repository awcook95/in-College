import settings
import states
import users


def enterInitialMenu():
    while settings.currentState == states.loggedOut:
        # success story
        print("\nNathan Cooper had always dreamed about getting a software engineering job after graduating from college.\n"
              "However, with no work history and no connections, he feared that finding a company to hire him after graduation\n"
              "would be difficult. After using inCollege, Nathan was able to connect with other students in the same major to\n"
              "discuss school, jobs, salaries, offers, and projects. He was also able to learn new skills that would increase\n"
              "his experience and improve the look of his resume.\n")

        print("Select Option:")
        print("1. Log in with existing account")
        print("2. Create new account")
        print("3. Find someone you know")
        print("4. Play a video")
        print("5. Quit")

        response = input()
        if response == '1':
            settings.currentState = states.login
        elif response == '2':
            settings.currentState = states.createAccount
        elif response == '3':
            settings.currentState = states.userSearch
        elif response == '4':
            print("Video is now playing\n")
        elif response == '5':
            settings.currentState = states.quit
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


def enterMainMenu():
    # Present the user with an introductory menu
    while settings.currentState == states.mainMenu:
        print("Options:\n"
              "1. Search for a job/internship\n"
              "2. Post a job\n"
              "3. Find someone you know\n"
              "4. Learn a new skill\n"
              "5. Logout")
        response = input()
        if response == '1':
            print("Under Construction")
        elif response == '2':
            settings.currentState = states.createJob
        elif response == '3':
            settings.currentState = states.userSearch
        elif response == '4':
            settings.currentState = states.selectSkill
        elif response == '5':
            users.logOutUser()
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue


def enterSkillMenu():
    # Skills menu will display under construction menus and return status
    while settings.currentState == states.selectSkill:
        print("What skill would you like to learn?:\n"
              "1. Python\n"
              "2. How to make a resume\n"
              "3. Scrum\n"
              "4. Jira\n"
              "5. Software Engineering\n"
              "6. None - return to menu")
        response = input()
        if response == '1':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '2':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '3':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '4':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '5':
            print("Under Construction")
            return True  # Searched for skill successfully
        elif response == '6':
            if not settings.signedIn:
                settings.currentState = states.loggedOut
            else:
                settings.currentState = states.mainMenu
            return False  # Don't learn skill
        else:
            print("Invalid Option, enter the number option you want and press enter")
            continue
