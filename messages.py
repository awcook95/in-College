from collections import namedtuple
import constants
import database as db
import settings
import states


def messageCenterMenu(dbCursor, dbConnection):
    print("Select a messaging option:\n"
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
    else:
        Message = namedtuple('User', 'message_id sender_uname receiver_uname body read')
        for i in range(0, len(messages)):
            # first create message object to select from
            selectedMessage = Message._make(messages[i])
            if selectedMessage.read == 0:
                print(f"{i+1}. {selectedMessage.sender_uname} (Unread)")
            else:
                print(f"{i+1}. {selectedMessage.sender_uname} ")

        print("\n")
        if len(messages) > 1:
            choice = input("Select a message 1 - " + str(len(messages)) + " to read: \n(Or press enter to return to previous menu)\n")
        else:
            choice = input("Enter '1' to read this message\n(Or press enter to return to previous menu)\n")
        if choice == "":
            settings.currentState = states.messageCenter  # returns to main() w/ currentState = messageCenter
            return
        try:
            int(choice)
        except ValueError:
            print("Invalid input\n")
            return
        if int(choice) not in range(1, len(messages) + 1):
            print("Invalid input\n")
            return

        selectedMessage = Message._make(messages[int(choice) - 1])
        print(f"{selectedMessage.body}\n")  # Print Message
        db.updateMessageAsRead(dbCursor, selectedMessage.message_id)  # Mark message as read
        dbConnection.commit()

        response = input(f"Would you like to send a reply to {selectedMessage.sender_uname}? (Y/N): ")
        if response.upper() == 'Y':
            reply = input(f"Enter message to {selectedMessage.sender_uname}: ")
            db.insertMessage(dbCursor, settings.signedInUname, selectedMessage.sender_uname, reply)  # Add new message
            dbConnection.commit()
            print("Message Sent")

        option = input(f"Would you like to delete {selectedMessage.sender_uname}'s message? (Y/N): ")
        if option.upper() == 'Y':
            db.deleteMessage(dbCursor, selectedMessage.message_id)  # Delete Message
            dbConnection.commit()
            print("Message Deleted")


def sendMessageMenu(dbCursor, dbConnection):
    friends = db.getUserFriends(dbCursor, settings.signedInUname)
    allUsers = db.getAllOtherUsers(dbCursor, settings.signedInUname)
    choice = "A"
    users = friends
    while True:
        if choice.upper() == "A":
            print("Your friends:")
        elif choice.upper() == "B":
            print("All InCollege users:")
        if len(users) > 0:
            for i in range(0, len(users)):
                user = namedtuple('user', 'uname pword firstname lastname plus_member')
                selectedUser = user._make(users[i])
                print(f"{i + 1}. {selectedUser.firstname} {selectedUser.lastname}")
        else:
            if choice.upper() == "A":
                print("None, go add some friends!:\n")
            elif choice.upper() == "B":
                print("No InCollege users found.\n")

        choice = input("{selectionRange}"
            "A. View my friends\n"
            "B. View all InCollege users\n"
            "Z. Return to previous menu\n"
            "input: ".format(selectionRange="\nSelect a user 1 - " + str(len(users)) + " to message: \n\n" if len(users) > 1 else "Enter '1' to message this user\n\n" if len(users) == 1 else "")
        )

        if choice.upper() == "A":
            users = friends
            continue
        elif choice.upper() == "B":
            users = allUsers
            continue
        elif choice.upper() == "Z":
            settings.currentState = states.messageCenter
            return
        try:
            int(choice)
        except ValueError:
            print("Invalid input")
            continue

        if len(users) == 0:
            print("Invalid input")
            continue

        if int(choice) not in range(1, len(users) + 1):
            print(f"Input must be 1 through {len(users) + 1}")
            continue

        user = namedtuple('user', 'uname pword firstname lastname plus_member')
        selectedUser = user._make(users[int(choice) - 1])

        if not db.checkUserFriendRelation(dbCursor, settings.signedInUname, selectedUser.uname) and not db.userIsPlusMember(dbCursor, settings.signedInUname):
            print("I'm sorry, you are not friends with that person -- Only InCollege Plus members may send messages to non-friends.")
            continue

        message = input(f"Enter your message you would like to send to {selectedUser.uname}: ")
        db.insertMessage(dbCursor, settings.signedInUname, selectedUser.uname, message)
        dbConnection.commit()
        print("Message sent")
