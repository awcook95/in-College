import states

currentState = states.loggedOut  # currentState tracks where we are in the program

signedIn = False      # tracks whether a user is signed in
signedInUname = None  # tracks name of a signed in user

# 1 = True; 0 = False for below settings
emailNotif = 1        # tracks user's email notification preference
smsNotif = 1          # tracks user's sms notification preference
targetAdvert = 1      # tracks user's targeted advertising preference
language = "English"  # tracks user's language preference
