import pathlib

# Create account class according to epic documentation 
class StudentAccount:
    username = ""
    password = ""
    def __init__(self, uname, passwrd):
        self.username = uname
        self.password = passwrd

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
def createStudentAccounts() : 
    acc_path = pathlib.Path("studentAccouts.txt")
    # check if file exists
    if not acc_path.exists():
        print("Account file not found! No action required.")
        return False

    acc_file = open("studentAccouts.txt", "r")
    # create array to be filled with accounts 
    student_accounts = []
    # assume correct formatting of file text, ===== seperators between objects
    while True:
        # get user and password check for eof
        username = acc_file.readline().split("\n")[0] # remove newline char
        password = acc_file.readline().split("\n")[0]
    
        student_accounts.append(StudentAccount(username, password))
        # check for end of file
        if acc_file.read(1) == '':
            print("eof\n")
            break
        # consume seperator chars
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
        return False
    
    job_file = open("newJobs.txt", "r")

    # create array to be filled with jobs 
    new_jobs = []

    # keep track of potential first char of title to ensure not lost when processing file
    title_start = ""
    
    # assume correct formatting of file text, ===== seperators between objects
    while True:
        # get all job attributes then check for eof 
        title = title_start + job_file.readline().split("\n")[0] # remove newline char, add first char that was potentially consumed

        lines = []
        # collect first decsription line and add to list of potential multiple lines
        line = job_file.readline().split("\n")[0]
        lines.append(line)
        while line != "=====": # read until end of record  
            line = job_file.readline().split("\n")[0]
            lines.append(line)

        desc_end = -1
        if "&&&" in lines: # check for multi-line descrition
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
            print("eof\n")
            break
        else: 
            # if next char isnt eof then need to keep it as part of next job title
            title_start = next_char 
    
    return new_jobs

# Endpoint for creating trainings (GET)
# This function reads in entire file, account creation limit logic will be handled elsewhere
# Assuming that if only one record exists it will be terminated by =====
def createTrainings(): 
    # assuming that file naming convention should be kept
    # file will be titled newTrainings, not newtrainings
    training_path = pathlib.Path("newTrainings.txt")
    # check if file exists
    if not training_path.exists():
        print("Training file not found! No action required.")
        return False

    train_file = open("newTrainings.txt", "r")
    # create array to be filled with accounts 
    trainings = []
    # assume correct formatting of file text, ===== seperators between objects
    while True:
        # get user and password check for eof
        title = train_file.readline().split("\n")[0] # remove newline char
        
        trainings.append(title)
        # check for end of file
        if train_file.read(1) == '':
            print("eof\n")
            break
        # consume seperator chars
        sep = train_file.readline()
    
    return trainings



##### THIS SECTION USED FOR TESTING ####
def main():
    # student_accounts = createStudentAccounts()
    # for obj in student_accounts:
    #     print(obj.username + " " + obj.password)
    # print("\n")

    # new_jobs = createJobs()
    # for obj in new_jobs:
    #     print(obj.title + "\n" + obj.description + "\n" + obj.employer_name + "\n" + obj.location + "\n" + obj.salary + "\n")

    trainings = createTrainings()
    if trainings:
        for obj in trainings:
            print(obj)
        print("\n")


if __name__ == "__main__":
    main()