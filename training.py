import database as db
import settings
import states
import constants


def trainingMenu(dbCursor, dbConnection):
    while settings.currentState == states.training:
        # displayed menu options
        print("\nTraining Menu:")
        print("A. Training and Education")
        print("B. IT Help Desk")
        print("C. Business Analysis and Strategy")
        print("D. Security")
        print("Z. Return to Previous Menu")
        response = input("Input: ")
        if response.upper() == "A":
            while True:
                # displayed menu options
                print("\nSelect a Training Course:")
                print("A. Products and Services Training")
                print("B. Quality Training")
                print("C. Safety Training")
                print("D. Team Training")
                print("Z. Return to Previous Menu")
                response = input("Input: ")
                if response.upper() == "A":
                    print("Under Construction")
                elif response.upper() == "B":
                    print("Under Construction")
                elif response.upper() == "C":
                    print("Under Construction")
                elif response.upper() == "D":
                    print("Under Construction")
                elif response.upper() == "Z":
                    break
                else:
                    print(constants.INVALID_INPUT)
        elif response.upper() == "B":
            print("Coming Soon!")
        elif response.upper() == "C":
            while True:
                # displayed menu options
                print("\nTrending Courses:")
                print("A. How to Use InCollege Learning")
                print("B. Train the Trainer")
                print("C. Gamification of Learning")
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
            print("Coming Soon!")
        elif response.upper() == "Z":
            settings.currentState = states.loggedOut        # returns user back to loggedOut menu
        else:
            print(constants.INVALID_INPUT)


def enterLearningMenu(dbCursor, dbConnection):
    while settings.currentState == states.learning:
        courses_completed = [db.getUserCompletedCourseByTitle(dbCursor, settings.signedInUname, "How to Use InCollege Learning"),
                             db.getUserCompletedCourseByTitle(dbCursor, settings.signedInUname, "Train the Trainer"),
                             db.getUserCompletedCourseByTitle(dbCursor, settings.signedInUname, "Gamification of Learning"),
                             db.getUserCompletedCourseByTitle(dbCursor, settings.signedInUname, "Understanding the Architectural Design Process"),
                             db.getUserCompletedCourseByTitle(dbCursor, settings.signedInUname, "Project Management Simplified")]
        print("\nInCollege Learning:")
        print(f"A. How to Use InCollege Learning{' (Completed)' if courses_completed[0] else ''}")
        print(f"B. Train the Trainer{' (Completed)' if courses_completed[1] else ''}")
        print(f"C. Gamification of Learning{' (Completed)' if courses_completed[2] else ''}")
        print(f"D. Understanding the Architectural Design Process{' (Completed)' if courses_completed[3] else ''}")
        print(f"E. Project Management Simplified{' (Completed)' if courses_completed[4] else ''}")
        # insert a more option that includes all of the new trainings or adaptive starting at 6 change original to 1 - 5
        print("Z. Return to Previous Menu")
        response = input("Input: ")
        if response.upper() == "A":
            handleCourse(dbCursor, courses_completed[0], "How to Use InCollege Learning")
        elif response.upper() == "B":
            handleCourse(dbCursor, courses_completed[1], "Train the Trainer")
        elif response.upper() == "C":
            handleCourse(dbCursor, courses_completed[2], "Gamification of Learning")
        elif response.upper() == "D":
            handleCourse(dbCursor, courses_completed[3], "Understanding the Architectural Design Process")
        elif response.upper() == "E":
            handleCourse(dbCursor, courses_completed[4], "Project Management Simplified")
        elif response.upper() == "Z":
            settings.currentState = states.mainMenu
        else:
            print(constants.INVALID_INPUT)


def handleCourse(dbCursor, course_completed, course_name):
    if not course_completed:
        print("You have now completed this training.")
        db.insertUserCompletedCourse(dbCursor, settings.signedInUname, course_name)
    else:
        choice = input("You have already taken this course, do you want to take it again? Enter 'Y' for yes or anything else to cancel: ")
        if choice.upper() == "Y":
            print("You have now completed this training.")
        else:
            print("Course cancelled.")

def insertCourse(dbCursor, course_name):
    db.insertNewCourse(dbCursor, course_name)
