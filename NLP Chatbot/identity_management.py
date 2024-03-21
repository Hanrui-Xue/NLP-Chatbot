from time import sleep
from processing import string_processing
from intent_matching import compare_intent

# Initial dialog and name initialisation
def intro(chatbot_name, intent_threshold):
    # Introduction Dialog on chatbot start
    bot_intro("---------------------------------", "------CHATBOT INITIALISING------\n")
    bot_intro("     o==[]::::::::::::::::>", "---------------------------------")
    print(f"Welcome O Brave Hero! My name is {chatbot_name}. Please converse with me.\n")
    print(f"{chatbot_name}: May I please know your good name?")

    # Loop to assignment name assignment
    while True:
        # user input for name
        temp_name = input("Nameless Hero: ")

        # ERROR CHECKING: EMPTY NAME
        # If username is not empty, pre-process and set as username
        if temp_name.strip():
            username = process_name(temp_name)
            print(f"{chatbot_name}: So...your name is {username}? ...truly a legendary name! Say anything, for example, \"How are you?\".")
            return username
        # Checks confirmation that user wants no name
        else:
            print(f"{chatbot_name}: No name? Are you sure? Say yes/no. If not, I will make up one for you.")
            # Intent similarity for checking if user says "yes" or similar
            name_confirm = input("Nameless Hero: ")
            intent = compare_intent(name_confirm.lower(), intent_threshold)
            # If intent matches ID accept patterns
            if ('accept' in intent):
                username = 'NH'
                print(f"{chatbot_name}: Ah secretive...a wise choice...I shall call you {username}!")
                return username
            else:
                print(f"{chatbot_name}: Please tell me your name!")


# Prints initial dialog
def bot_intro(bot_text1, bot_text2):
    print(bot_text1)
    sleep(1)
    print(bot_text2)
        

# Processes name when inputted by user and capitalizes, uses string_processing (pre-processing)
def process_name(query):
    # Process the name, removes stop words
    names = string_processing(query, False)

    # Split by space for list
    names = names.split()

    # If there is an entity chars greater than 15, then remove it (for user experience)
    for name in names:
        if len(name) > 15:
            names.remove(name)

    # Capitalize all entities in the list
    names = [name.capitalize() for name in names]

    # Check if user input more than one string, allows up to two words in a name
    return f"{names[0]} {names[1]}" if len(names) > 1 else names[0]
    

def change_name(intent, username, chatbot_name):
    new_username = None
    print("---------------------------------------")
    print(f"{chatbot_name}: What would you like your new name to be, Hero?")
    new_username = input(f"{username} will now become...: ")
    # If new username is empty, then assume user wants to keep name
    if new_username.strip() == '':
        print(f"{chatbot_name}: Oh, you want to keep your name! I'm truly glad {username}.")
    else:
        # Pre-process name
        new_username = process_name(new_username)
        # Adds intent response to new username to form an answer
        answer = intent[1] + new_username
        # Sets new username
        username = new_username
        print(f"{chatbot_name}: {answer}. Of course the legend can be whatever he wants!")

    return username
