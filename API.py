import pathlib

# Create class according to epic documentation 
class StudentAccount:
    username = ""
    password = ""
    def __init__(self, uname, passwrd):
        self.username = uname
        self.password = passwrd

# Endpoint for creating student accounts (GET)
# This function reads in entire file, account creation limit logic will be handled elsewhere
def createStudentAccounts() : 
    acc_file = pathlib.Path("studentAccouts.txt")
    # Check if file exists
    if not acc_file.exists():
        print("Account file not found! No action required.")
        return 

    acc_file = open("studentAccouts.txt", "r")
    # Create array to be filled with accounts 
    student_accounts = []
    # Assume correct formatting of file text, ===== seperators between objects
    while True:
        # get user and password then determine if that is the last line
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


##### THIS SECTION USED FOR TESTING ####
def main():
    student_accounts = createStudentAccounts()
    for obj in student_accounts:
        print(obj.username + " " + obj.password)

if __name__ == "__main__":
    main()