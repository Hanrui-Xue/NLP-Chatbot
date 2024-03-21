
import datetime
from intent_matching import compare_intent

# Function for outputting an intent matching feeling for "How are you" in multi-turn dialogue
def feelings(intent, chatbot_name, username, intent_threshold):
    # Prints and checks if the intent response matches one of the two
    print(f"{chatbot_name}: {intent[1]}")
    if intent[1] in ['I am extremely tired today. What about you?', "What I feel doesn't matter! I'm more worried about you..."]:
        # If it matches then get user input and perform intent matching to check if the user response is positive and negative
        feelings_response = input(f"{username}: ")
        intent_feelings = compare_intent(feelings_response.lower(), intent_threshold)
        # Prints feeling according to user emotion inputted
        if ('feelings_user_positive' in intent_feelings) or ('feelings_user_negative' in intent_feelings):
            print(f"{chatbot_name}: {intent_feelings[1]}")
    return

# Function for outputting the time
def time_check(intent):
    # Retrieves current datetime
    current_time = datetime.datetime.now()
    # Formats the datetime and returns it with intent response
    time = intent[1] + current_time.strftime("%Y-%m-%d %H:%M:%S")
    return time