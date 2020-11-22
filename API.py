import pathlib
import database as db

# Create account class according to epic documentation 
class StudentAccount:
    username = ""
    password = ""
    first_name = ""
    last_name = ""
    plus_member = 0

    def __init__(self, uname, passwrd, first, last, plus):
        self.username = uname
        self.password = passwrd
        self.first_name = first
        self.last_name = last
        self.plus_member = plus

# Create job class according to epic documentation
class Job:
    title = ""
    description = ""  # multi-line ended by &&&, needs to be consumed and removed
    employer_name = ""
    location = ""
    salary = ""
    def __init__(self, title, desc, emp, loc, sal):
        self.title = title
        self.description = desc
        self.employer_name = emp
        self.location = loc
        self.salary = sal


# Endpoint for creating student accounts (GET)
# This function reads in entire file, account creation limit logic will be handled elsewhere
# Assuming that if only one record exists it will be terminated by =====
# Going off response from Dr. Anderson stating all fields required to create account should be present
def createStudentAccounts() : 
    acc_path = pathlib.Path("studentAccounts.txt")
    # check if file exists
    if not acc_path.exists():
        print("Account file not found! No action required.")
        return None

    acc_file = open("studentAccounts.txt", "r")
    # create array to be filled with accounts 
    student_accounts = []
    # assume correct formatting of file text, ===== separators between objects
    while True:
        # get user and password check for eof
        username = acc_file.readline().split("\n")[0] # remove newline char
        password = acc_file.readline().split("\n")[0]
        first_name = acc_file.readline().split("\n")[0]
        last_name = acc_file.readline().split("\n")[0]
        plus_member = acc_file.readline().split("\n")[0].strip()

        # extra "\n" is automatically inserted by text editor, shouldn't submit this empty record
        if(username != ""):
            student_accounts.append(StudentAccount(username, password, first_name, last_name, plus_member))

        # check for end of file
        if acc_file.read(1) == '':
            #print("eof\n")
            break
        # consume separator chars
        sep = acc_file.readline()

    return student_accounts


# Endpoint for creating jobs (GET)
# This function reads in entire file, job creation limit logic will be handled elsewhere
# Assuming that if only one record exists it will be terminated by =====
def createJobs():
    job_path = pathlib.Path("newJobs.txt")
    # check if file exists
    if not job_path.exists():
        print("Job file not found! No action required.")
        return None
    job_file = open("newJobs.txt", "r")

    # create array to be filled with jobs 
    new_jobs = []

    # keep track of potential first char of title to ensure not lost when processing file
    title_start = ""
    
    # assume correct formatting of file text, ===== separators between objects
    while True:
        # get all job attributes then check for eof 
        title = title_start + job_file.readline().split("\n")[0] # remove newline char, add first char that was potentially consumed

        lines = []
        # collect first description line and add to list of potential multiple lines
        line = job_file.readline().split("\n")[0]
        lines.append(line)
        while line != "=====": # read until end of record  
            line = job_file.readline().split("\n")[0]
            lines.append(line)

        desc_end = -1
        if "&&&" in lines: # check for multi-line description
            desc_end = lines.index("&&&")
        
        desc = ""
        emp = ""
        loc = ""
        sal = ""

        if(desc_end == -1): # not a multi-line description
            desc += lines[0]
            emp += lines[1]
            loc += lines[2]
            sal += lines[3]
        else: # multi-line description
            for i in range(0, desc_end, 1):
                desc += lines[i] + " " # concatenate all description lines
            
            start = desc_end + 1 # rest of job attributes start here
            emp += lines[start]
            loc += lines[start + 1]
            sal += lines[start + 2]

       
        new_jobs.append(Job(title, desc, emp, loc, sal))
        # check for end of file
        next_char = job_file.read(1)
        if next_char == '':
            #print("eof\n")
            break
        else: 
            # if next char isn't eof then need to keep it as part of next job title
            title_start = next_char 
    
    return new_jobs

# Endpoint for creating trainings (GET)
# This function reads in entire file, account creation limit logic will be handled elsewhere
# Assuming that if only one record exists it will be terminated by =====
def createTrainings(): 
    # assuming that file naming convention should be kept
    # file will be titled newTrainings, not new trainings
    training_path = pathlib.Path("newTrainings.txt")
    # check if file exists
    if not training_path.exists():
        print("Training file not found! No action required.")
        return False

    train_file = open("newTrainings.txt", "r")
    # create array to be filled with accounts 
    trainings = []
    # assume correct formatting of file text, ===== separators between objects
    while True:
        # get user and password check for eof
        title = train_file.readline().split("\n")[0] # remove newline char
        
        trainings.append(title)
        # check for end of file
        if train_file.read(1) == '':
            #print("eof\n")
            break
        # consume separator chars
        sep = train_file.readline()
    
    return trainings

# Outputs the jobs into the "MyCollege_jobs.txt" output API
def outputJobs(dbCursor):
    f = open("MyCollege_jobs.txt", "w+")
    # create list to be filled with jobs
    jobs = db.getAllJobs(dbCursor)
    for job in jobs:
        f.write(f"{job[1]}\n")      # Title
        f.write(f"{job[2]} &&&\n")  # Description
        f.write(f"{job[3]}\n")      # Employer
        f.write(f"{job[4]}\n")      # Location
        f.write(f"{job[5]}\n")      # Author
        f.write("=====\n")
    f.close()

# Outputs jobs and their applications into the "MyCollege_appliedJobs.txt output API 
def outputAppliedJobs(dbCursor):
    f = open("MyCollege_appliedJobs.txt", "w+")

    # create list to be filled with jobs 
    jobs = db.getAllJobs(dbCursor)

    for job in jobs:
        # get all applicants for this job
        applicants = db.getJobApplicationDetailsByTitle(dbCursor, job[1])

        # print job title and applicant info 
        f.write(f"{job[1]}\n")      # Title

        # print details of any applicants
        if applicants != None:
            for app in applicants:
                f.write(f"{app[0]}\n") # applicant name 
                f.write(f"{app[1]}\n") # credentials
        
        # write job posting separator 
        f.write("=====\n")

# Outputs saved jobs for each user 
def outputSavedJobsByUser(dbCursor):
    f = open("MyCollege_savedJobs.txt","w+")

    # create list of users
    users = db.getAllUsers(dbCursor)

    for user in users:
        jobs = db.getFavoriteJobsByUser(dbCursor, user[0]) # get "saved" jobs for user
        
        if jobs != None: # should only output users who have saved jobs
            f.write(f"{user[0]}\n") # username
            for job in jobs:
                f.write(f"{job[1]}\n") # job title

        f.write("=====") # output user separator


# Outputs the profile pages of students into the "MyCollege_profiles.txt" output API
def outputProfiles(dbCursor):
    f = open("MyCollege_profiles.txt", "w+")
    users = db.getAllUsers(dbCursor)
    for user in users:
        profile = db.getProfilePage(dbCursor, user[0])
        jobs = db.getProfileJobs(dbCursor, user[0])
        education = db.getProfileEducation(dbCursor, user[0])
        f.write(f"{user[2]} {user[3]}'s Profile Page\n")    # Title
        f.write(f"Major: {profile[1]}\n")                   # Major
        f.write(f"University: {profile[2]}\n")              # University Name
        f.write(f"About: {profile[3]}\n")                   # About
        f.write("Experience:\n")
        for job in jobs:                                    # Experience
            f.write(f"{job[2]}\n")                              # Title
            f.write(f"\tEmployer: {job[3]}\n")                  # Employer
            f.write(f"\tDate: {job[4]} - {job[5]}\n")           # Start Date - End Date
            f.write(f"\tLocation: {job[6]}\n")                  # Location
            f.write(f"\tDescription: {job[7]}\n")               # Job Description
        f.write("Education:\n")
        for edu in education:                               # Education
            f.write(f"University: {edu[2]}\n")                  # University Name
            f.write(f"\tDegree: {edu[3]}\n")                    # Degree
            f.write(f"\tYear: {edu[4]} - {edu[5]}\n")           # Start Year - End Year
        f.write("=====\n")
    f.close()

# Outputs the Usernames along with their account type into the "MyCollege_users.txt" output API
def outputUsers(dbCursor):
    f = open("MyCollege_users.txt", "w+")
    users = db.getAllUsers(dbCursor)
    for user in users:
        f.write(f"{user[0]} {'plus' if user[4] == 1 else 'standard'}\n")  # Username AccType
    f.close()


        ##### THIS SECTION USED FOR TESTING ####
#def main():
    # student_accounts = createStudentAccounts()
    # for obj in student_accounts:
    #     print(obj.username + " " + obj.password + " " + obj.first_name  + " " + obj.last_name + " " + obj.plus_member)

    # new_jobs = createJobs()
    # for obj in new_jobs:
    #     print(obj.title + "\n" + obj.description + "\n" + obj.employer_name + "\n" + obj.location + "\n" + obj.salary + "\n")

    # trainings = createTrainings()
    # if trainings:
    #     for obj in trainings:
    #         print(obj)
    #     print("\n")


# if __name__ == "__main__":
#     main()