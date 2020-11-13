import database as db
import settings
import states
import constants

def trainingMenu(dbCursor, dbConnection):
    while settings.currentState == states.training:
        # displayed menu options
        print("Training Menu:")
        print("A. Training and Education")
        print("B. IT Help Desk")
        print("C. Business Analysis and Strategy")
        print("D. Security")
        print("Z. Return to Previous Menu")
        response = input("Input: ")
        if response.upper() == "A":
            while True:
                # displayed menu options
                print("Select a training course")
                print("A. Products and Services Training")
                print("B. Quality Training")
                print("C. Safety Training")
                print("D. Team Training")
                print("Z. Return to Previous Menu")
                response = input("Input: ")
                if response.upper() == "A":
                    print("Under construction\n")
                elif response.upper() == "B":
                    print("Under construction\n")
                elif response.upper() == "C":
                    print("Under construction\n")
                elif response.upper() == "D":
                    print("Under construction\n")
                elif response.upper() == "Z":
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "B":
            print("Coming Soon!\n")
        elif response.upper() == "C":
            while True:
                # displayed menu options
                print("Trending Courses")
                print("A. How to use In College learning")
                print("B. Train the trainer")
                print("C. Gamification of learning")
                print("Z. Return to Previous Menu")
                print("Not seeing what you're looking for? Sign in to see all 7,609 results.")
                response = input("Input: ")
                if response.upper() == "A":
                    settings.currentState = states.login    # prompts user login
                    break
                elif response.upper() == "B":
                    settings.currentState = states.login    # prompts user login
                    break
                elif response.upper() == "C":
                    settings.currentState = states.login    # prompts user login
                    break
                elif response.upper() == "Z":
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "D":
            print("Coming Soon!\n")
        elif response.upper() == "Z":
            settings.currentState = states.loggedOut        # returns user back to loggedOut menu
        else:
            print(constants.INVALID_INPUT)