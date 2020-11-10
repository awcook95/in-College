import database as db
import constants
import settings
import states


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
