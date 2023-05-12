from pythmc import ChatLink
import time
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

def summarize_wikipedia(topic):
    page = wikipedia.page(topic)
    return wikipedia.summary(topic)

chat = ChatLink()  # Initialises an instance of ChatLink, to take control of the Minecraft Chat.
prev_msg = ""

import msvcrt
import time

def optional_input(time_limit=None):
    if time_limit is not None:
        print(f"Enter a value (press Enter to skip, timeout in {time_limit} seconds): ", end="")
        start_time = time.monotonic()
        while True:
            if msvcrt.kbhit():
                # user pressed a key, read input
                user_input = input()
                return user_input
            elif time.monotonic() - start_time > time_limit:
                # time limit exceeded
                return None
    else:
        # no time limit specified, use standard input()
        user_input = input("Enter a value (press Enter to skip): ")
        if user_input:
            # user provided a value
            return user_input
        else:
            # user did not provide a value
            return None

while True:
    msg = list(chat.get_history(limit=1))[0].content
    if msg != prev_msg:
        prev_msg = msg
        if msg.startswith("(From "):
            user = msg.split(":")[0][6:][:-1]
            msg = " ".join(msg.split(":")[1:]).strip().lower()
            if msg.startswith("fredos>"):
                msg = msg[7:].strip().lower()
                if msg == "":
                    command = ""
                else:
                    command = msg.split()[0].strip()
                if (command == "location"):
                    chat.send("/maplink")
                    time.sleep(2)
                    chats = list(chat.get_history(limit=100))
                    link = ""
                    for message in chats:
                        if message.content.startswith("http://www.cubeville.org/map/#"):
                            link = message.content
                    chat.send(rf"/msg {user} {list(chat.get_history(limit=1))[0].content}")
                elif (command == "summarize"):
                    msg = msg[10:]
                    print(msg)
                    try:
                        chat.send(rf"/msg {user} {summarize_wikipedia(msg)}")
                    except Exception as e:
                        print(e)
                        chat.send(rf"/msg {user} An error occurred. Sorry about that. Try a different topic.")
                elif (command == "help"):
                    chat.send(rf"/msg {user} FREDos v0.0.1 commands:")

                    chat.send(rf"/msg {user} location:")
                    chat.send(rf"/msg {user}     Generates a maplink to Frederick's location")

                    chat.send(rf"/msg {user} help:")
                    chat.send(rf"/msg {user}     Show this help message")
                else:
                    chat.send(rf"/msg {user} Try 'fredos> help' for a command list")