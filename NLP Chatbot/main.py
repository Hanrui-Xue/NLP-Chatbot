import sys
import nltk
import timeit

from identity_management import intro, change_name
from intent_matching import compare_intent
from processing import dataset_processing
from questions_retrieval import question_answering
from transaction import hotel_transaction
from small_talk import feelings, time_check

#REFERENCE Benchmarking: Campbell, S. (2022) Python timeit() with examples, Guru99. Available at: https://www.guru99.com/timeit-python-examples.html. 

# MAIN FUNCTION
def main():
    # Download NLTK Packages necessary 
    download_nltk_data()
    
    chatbot_name = 'Bam'

    #Declares intent and question + answer thresholds for similarities
    intent_threshold = 0.75
    QA_threshold = 0.5
    # Intital dialogue and setting name
    username = intro(chatbot_name, intent_threshold)

    # MAIN LOOP: user input for intent matching
    while True:
        query = input(f"{username}: ")
        # BENCHMARKING
        #starttime = timeit.default_timer()
        #print("Start time:",starttime)
        # INTENT MATCHING
        intent = compare_intent(query.lower(), intent_threshold)
        #print("Time difference:", timeit.default_timer() - starttime)
        # If the similarity value does not exceed the intent_threshold go to QA
        if None in intent:
            # Processes the COMP3074-CW1-Dataset.csv dataset
            dataset_processing()
            info_retrieval = question_answering(query, QA_threshold)
            print(f"{chatbot_name}: {info_retrieval}")

        ## INTENT MATCHING: if the intent matches...
        # Exits program
        elif ('cancellation' in intent or 'exit' in intent):
            quit_program(chatbot_name, username, intent, intent_threshold)

        # Initiates hotel transaction
        elif ('transaction' in intent[0]):
            hotel_transaction(chatbot_name, username, intent_threshold)

        # Asks chatbot's hobbies
        elif ('hobbies' in intent):
            print(f"{chatbot_name}: {intent[1]}")

        # Asks chatbot's favourite food
        elif ('fav_food' in intent):
            print(f"{chatbot_name}: {intent[1]}")     

        # Program instructions
        elif ('purpose' in intent):
            print(f"{chatbot_name}: {intent[1]}")     

        # Asks for chatbot's feelings    
        elif ('feelings_bot' in intent):
            feelings(intent, chatbot_name, username, intent_threshold)

        # Identity management, if ID in json has "name" in it
        elif ('name' in intent[0]):
            # Changes username
            if ('name_change' in intent):
                username = change_name(intent, username, chatbot_name)
            # Repeats back username
            elif ('name_check' in intent):
                answer = intent[1] + username
                print(f"{chatbot_name}: {answer}" + ", my liege. Please don't forget!")
        else:  
            # Sets answer as intent
            answer = intent[1]
            #Checks current datetime
            if ('time' in intent):
                answer = time_check(intent)
            print(f"{chatbot_name}: {answer}")
        print("---------------------------------------")

# Function for downloading NLTK modules
def download_nltk_data():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')
    nltk.download('omw-1.4')
    nltk.download('stopwords')

# Function for program exit
def quit_program(chatbot_name, username, intent, intent_threshold):
    # Prompt the user to confirm their exit
    print(f"{chatbot_name}: I enjoyed our conversation so much. You sure you want to leave?")
    confirm_exit = input(f"{username}: ")
    intent = compare_intent(confirm_exit.lower(), intent_threshold)
    # If yes: Quit
    if ('accept' in intent):
        print(f"{chatbot_name}: It was an honour, {username}.")
        sys.exit()
    # If no: Program continues back to main loop
    elif ('decline' in intent):
        print(f"{chatbot_name}: I knew I could count on you!")

# calls main function
if __name__ == "__main__":
    main()

