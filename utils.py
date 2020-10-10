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
