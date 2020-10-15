from collections import namedtuple
import dbfunctions as db
import settings


def validatePassword(password):
    if len(password) < 8 or len(password) > 12:     # out of length bounds
        return False
    elif not any(x.isupper() for x in password):    # no capital letter
        return False
    elif not any(x.isnumeric() for x in password):  # no digits
        return False
    elif not any(x.isalnum() for x in password):    # non alphanumeric
        return False
    else:
        return True


def printUserFriends(dbCursor, uname):
    friends = db.getUserFriendsByName(dbCursor, uname)
    if friends:
        count = 1
        for f in friends:
            print(f"{count}. {f[0]}")
            count += 1
        return friends
    else:
        return None

def handleUserFriendRequests(dbCursor, dbConnection, reciever):
    requests = db.getUserFriendRequests(dbCursor, reciever) # Check for pending request

    if len(requests) > 0: 
        for r in requests: 
            print("Request from: " + r[0] + "\n" )
            response = input("Would you like to Accept (A) or Ignore (I): ")
            while(response.upper() != 'A' or response != 'I'):
                if(response.upper() == 'A'):
                    # To accept will add friend relation to both users
                    db.insertUserFriend(dbCursor, settings.signedInUname, r[0])
                    db.insertUserFriend(dbCursor, r[0], settings.signedInUname)
                    # Delete existing request and commit changes
                    db.deleteFriendRequest(dbCursor, r[0], settings.signedInUname)
                    dbConnection.commit()
                    break
                elif(response.upper() == 'I'):
                    break
                else: 
                    print("Invalid input: enter either A to accept or I to ignore")
                    response = input("Would you like to Accept (A) or Ignore (I): ")

        return requests
    else: 
        return None

# Searches through existing friend requests to determine if the one you are attempting to send 
# has already been sent, to avoid duplicate records
def checkExistingFriendRequest(dbCursor, sender, reciever):
    requests = db.getUserFriendRequests(dbCursor, reciever)
    exists = False
    if len(requests) > 0:
        for r in requests:
            Request = namedtuple('Request', 'sender_uname reciever_uname')
            f = Request._make(r)
            # Found matching request, shouldn't create a duplicate
            if f.sender_uname == sender and f.reciever_uname == reciever:
                exists = True

    return exists 

