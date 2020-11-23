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
                print("\nSelect a Training training:")
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
                print("\nTrending trainings:")
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
        trainings = db.getAllTrainings(dbCursor)
        trainings_completed = [db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, "How to Use InCollege Learning"),
                               db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, "Train the Trainer"),
                               db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, "Gamification of Learning"),
                               db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, "Understanding the Architectural Design Process"),
                               db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, "Project Management Simplified")]

        # appends new trainings from the newTrainings.txt API into the list of trainings
        for obj in trainings:
            trainings_completed.append(db.getUserCompletedTrainingByTitle(dbCursor, settings.signedInUname, obj[1]))

        print("\nInCollege Learning:")
        print(f"1. How to Use InCollege Learning{' (Completed)' if trainings_completed[0] else ''}")
        print(f"2. Train the Trainer{' (Completed)' if trainings_completed[1] else ''}")
        print(f"3. Gamification of Learning{' (Completed)' if trainings_completed[2] else ''}")
        print(f"4. Understanding the Architectural Design Process{' (Completed)' if trainings_completed[3] else ''}")
        print(f"5. Project Management Simplified{' (Completed)' if trainings_completed[4] else ''}")
        for obj in trainings:
            print(f"{obj[0] + 5}. {obj[1]}{' (Completed)' if trainings_completed[obj[0] + 4] else ''}")
        print("Z. Return to Previous Menu")
        response = input("Input: ")
        if response == "1":
            handleTraining(dbCursor, trainings_completed[0], "How to Use InCollege Learning")
        elif response == "2":
            handleTraining(dbCursor, trainings_completed[1], "Train the Trainer")
        elif response == "3":
            handleTraining(dbCursor, trainings_completed[2], "Gamification of Learning")
        elif response == "4":
            handleTraining(dbCursor, trainings_completed[3], "Understanding the Architectural Design Process")
        elif response == "5":
            handleTraining(dbCursor, trainings_completed[4], "Project Management Simplified")
        elif response.isdigit() and 6 <= int(response) <= len(trainings_completed):    # Lists all new training options here
            handleTraining(dbCursor, trainings_completed[int(response) - 1], (trainings[int(response) - 6])[1])
        elif response.upper() == "Z":
            settings.currentState = states.mainMenu
        else:
            print(constants.INVALID_INPUT)


def handleTraining(dbCursor, training_completed, training_name):
    if not training_completed:
        print("You have now completed this training.")
        db.insertUserCompletedTraining(dbCursor, settings.signedInUname, training_name)
    else:
        choice = input("You have already taken this training, do you want to take it again? Enter 'Y' for yes or anything else to cancel: ")
        if choice.upper() == "Y":
            print("You have now completed this training.")
        else:
            print("Training cancelled.")
