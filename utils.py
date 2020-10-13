from collections import namedtuple
import dbfunctions as db


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

def printUserFriendRequests(dbCursor, reciever):
    requests = db.getUserFriendRequests(dbCursor, reciever)
    if len(requests) > 0: 
        count = 1
        for r in requests: 
            print("Request from: " + r[0] )
            count += 1
        return requests
    else: 
        return None

# Searches through existing friend requests to determine if the one you are attempting to send 
# has already been sent, to avoid duplicate records
def checkExistingFriendRequest(dbCursor, sender, reciever):
    requests = db.getUserFriendRequests(dbCursor, reciever)
    exists = False
    if requests:
        for r in requests:
            Request = namedtuple('Request', 'relation_id sender_uname reciever_uname')
            f = Request._make(r)
            # Found matching request, shouldn't create a duplicate
            if f.sender_uname == sender and f.reciever_uname == reciever:
                exists = True

    return exists 

