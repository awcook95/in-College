import constants
import database as db
import settings
import states


def messageCenterMenu(dbCursor, dbConnection):
    print("\nSelect a messaging option:\n"
          "A. Inbox\n"
          "B. Send Message\n"
          "Z. Return to Previous Menu")
    while settings.currentState == states.messageCenter:
        choice = input("Input: ")
        if choice.upper() == "A":
            settings.currentState = states.inbox        # returns to main() w/ currentState = inbox
        elif choice.upper() == "B":
            settings.currentState = states.sendMessage  # returns to main() w/ currentState = sendMessage
        elif choice.upper() == "Z":
            settings.currentState = states.mainMenu     # returns to main() w/ currentState = mainMenu
        else:
            print(constants.INVALID_INPUT)


def inboxMenu(dbCursor, dbConnection):
    # Display list of messages
    messages = db.getMessageByReceiver(dbCursor, settings.signedInUname)
    if len(messages) == 0:
        print("You have no messages.")
        settings.currentState = states.messageCenter
        return

    print()
    for i in range(0, len(messages)):
        # first create message object to select from
        currentMessage = constants.MESSAGE_TUPLE._make(messages[i])
        if currentMessage.read == 0:
            print(f"{i + 1}. {currentMessage.sender_uname} (Unread)")
        else:
            print(f"{i + 1}. {currentMessage.sender_uname}")

    print("#. Choose one of the above messages to read")
    print("Z. Return to Previous Menu")

    while True:
        response = input("Input: ")
        if response.isdigit() and 1 <= int(response) <= len(messages):
            selectedMessage = messages[int(response) - 1]
            viewMessage(dbCursor, dbConnection, selectedMessage)
            break
        elif response.upper() == "Z":
            settings.currentState = states.messageCenter
            break
        else:
            print(constants.INVALID_INPUT)


def viewMessage(dbCursor, dbConnection, selectedMessage):
    selectedMessage = constants.MESSAGE_TUPLE._make(selectedMessage)

    while True:
        print(f"\n{selectedMessage.sender_uname}'s Message:")
        print(selectedMessage.body)
        if selectedMessage.read == 0:  # if message was previously unread
            db.updateMessageAsRead(dbCursor, selectedMessage.message_id)  # mark message as read
            dbConnection.commit()

        print("A. Reply")
        print("B. Delete Message")
        print("Z. Return to Previous Menu")

        while True:
            response = input("Input: ")
            if response.upper() == "A":
                reply = input(f"Enter message to {selectedMessage.sender_uname}: ")
                db.insertMessage(dbCursor, settings.signedInUname, selectedMessage.sender_uname, reply)
                dbConnection.commit()
                print("Reply successfully sent.")
                break
            elif response.upper() == "B":
                db.deleteMessage(dbCursor, selectedMessage.message_id)
                dbConnection.commit()
                print("Message successfully deleted, returning to previous menu.")
                return
            elif response.upper() == "Z":
                return
            else:
                print(constants.INVALID_INPUT)


def sendMessageMenu(dbCursor, dbConnection):
    friends = db.getUserFriends(dbCursor, settings.signedInUname)
    allUsers = db.getAllOtherUsers(dbCursor, settings.signedInUname)
    choice = "A"
    users = friends
    while True:
        if choice.upper() == "A":
            print("\nYour Friends:")
        elif choice.upper() == "B":
            print("\nAll InCollege Users:")

        if len(users) > 0:
            for i in range(0, len(users)):
                selectedUser = constants.USER_TUPLE._make(users[i])
                print(f"{i + 1}. {selectedUser.firstname} {selectedUser.lastname}")
        else:
            if choice.upper() == "A":
                print("None, go add some friends!")
            elif choice.upper() == "B":
                print("No other InCollege users found.")

        print("\n#. Choose a user to message")
        print("A. View Friends")
        print("B. View All InCollege Users")
        print("Z. Return to Previous Menu")

        while True:
            response = input("Input: ")
            if response.isdigit() and 1 <= int(response) <= len(users):
                selectedUser = constants.USER_TUPLE._make(users[int(response) - 1])
                if not db.checkUserFriendRelation(dbCursor, settings.signedInUname, selectedUser.uname) and not db.userIsPlusMember(dbCursor, settings.signedInUname):
                    print("I'm sorry, you are not friends with that person -- Only InCollege Plus members may send messages to non-friends.")
                    continue

                message = input(f"Enter message to {selectedUser.uname}: ")
                db.insertMessage(dbCursor, settings.signedInUname, selectedUser.uname, message)
                dbConnection.commit()
                print("Message successfully sent.")
                break
            elif response.upper() == "A":
                users = friends
                choice = "A"
                break
            elif response.upper() == "B":
                users = allUsers
                choice = "B"
                break
            elif response.upper() == "Z":
                settings.currentState = states.messageCenter
                return
            else:
                print(constants.INVALID_INPUT)
