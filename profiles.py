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
                    print(constants.INVALID_INPUT)
                    continue
        elif response.upper() == 'Z':
            settings.currentState = states.mainMenu
            return False  # No links chosen
        else:
            print(constants.INVALID_INPUT)
            continue


def printProfilePage(dbCursor, uname):
    name = db.getUserByName(dbCursor, uname)
    page = db.getProfilePage(dbCursor, uname)
    jobs = db.getProfileJobs(dbCursor, uname)
    education = db.getProfileEducation(dbCursor, uname)

    print(f"{name[2]} {name[3]}'s Profile Page")  # name[2] = user first name; name[3] = user last name
    print(f"Major: {page[1]}")                    # page[1] = user major
    print(f"University: {page[2]}")               # page[2] = user university
    print(f"About: \n{page[3]}")                  # page[3] = user about
    if jobs is None:
        print("Career:")
    else:
        print("Career:")
        for job in jobs:
            print(job[2])                          # job[2] = job title
            print(f"\tEmployer: {job[3]}")         # job[3] = job employer
            print(f"\tDate: {job[4]} - {job[5]}")  # job[4] = job start date; job[5] = job end date
            print(f"\tLocation: {job[6]}")         # job[6] = job location
            print(f"\tDescription: \n\t{job[7]}")  # job[7] = job description

    if education is None:
        print("Education:")
    else:
        print("Education:")
        for i in education:
            print(f"University: {i[2]}")       # i[2] = university name
            print(f"\tDegree: {i[3]}")         # i[3] = degree
            print(f"\tYear: {i[4]} - {i[5]}")  # i[4] = start year; i[5] = end year

    return page[1], page[2], page[3]
