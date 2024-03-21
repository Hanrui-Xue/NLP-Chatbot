import requests

from bs4 import BeautifulSoup
from intent_matching import compare_intent

# REFERENCE HELP for webscraping with BeautifulSoup: 
# Paruchuri, V. (2021) Tutorial: Web scraping with python using beautiful soup, Dataquest. 
# Available at: https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/. 

# Makes a transaction on uk.hotels.com using webscraping according to user inputs
def hotel_transaction(chatbot_name, username, intent_threshold):
    # Defines web browser and OS that is used to make the request
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    print("--------------------------------------------------")
    print(f"{chatbot_name}: Let's go travelling!! Leave the transaction by saving \"exit\" at any time.")

    # Start of entire transaction loop, returns to starting point if required
    transaction_flag = True
    while transaction_flag:
        # Start of transaction questions
        print(f"{chatbot_name}: How many adults should I put in, my liege?")
        adults = input(f"{username}: ")

        child_string = ""
        count = 0

        # Loop to add children to booking
        have_child = True
        while have_child:
            print(f"{chatbot_name}: Do we have future warriors? Input the child's age. If none/no more then say skip.")
            child_input = input(f"{username}: ")
            # Stops inputting children if skip
            if child_input in ["skip", "no", "none"]:
                have_child=False
            # Due to URl formatting, the first child is 1_(AGE), assigned using count, and the subsequent ones are 2C1_(AGE)
            elif (child_input.isdigit()):
                child_string += f"1_{child_input}" if count < 1 else f"%2C1_{child_input}"
            else:
                print("Sorry! I don't understand. What's the age of the child? Or \"skip\"?")
            count+=1

        # Replaces / and . with correct - format, common alternative formats for dates
        print(f"{chatbot_name}: What date is the Hero checking in? (yyyy-mm-dd)")
        date_in = input(f"{username}: ").replace("/", "-").replace(".", "-")

        print(f"{chatbot_name}: What about your check out date? (yyyy-mm-dd)")
        date_out = input(f"{username}: ").replace("/", "-").replace(".", "-")

        print(f"{chatbot_name}: Where are we conquering?")
        destination = input(f"{username}: ")
        print("")

        # Inputs user inputs as parameters into end of URL
        user_input_url = f'adults={adults}&children={child_string}&d1={date_in}&d2={date_out}&destination={destination}'

        # Concatenate URL based on user inputs
        url = f'https://uk.hotels.com/Hotel-Search?{user_input_url}'

        # Sends a get request to url
        # Parse HTML content with Python's built-in HTML parser and create object
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")

        # Retrieve HTML data from website 
        # Counter to error check if 0 results
        inspect_hotel_names = soup.find_all('h2', attrs={'class':'uitk-heading uitk-heading-5 overflow-wrap'})
        counter0 = sum(1 for _ in inspect_hotel_names)
        hotel_names = [name.text for name in inspect_hotel_names]

        inspect_hotel_prices = soup.find_all('span', attrs={'data-stid':'price-lockup-text'}) #class: uitk-lockup-price
        counter1 = sum(1 for _ in inspect_hotel_names)
        hotel_prices = [price.text for price in inspect_hotel_prices]

        inspect_hotel_nights = soup.find_all('div', attrs={'class':'uitk-price-subtext uitk-price-subtext-unpadded'})
        counter2 = sum(1 for _ in inspect_hotel_names)
        hotel_nights = [night.text for night in inspect_hotel_nights]

        inspect_hotel_rating = soup.find_all('span', attrs={'class': 'uitk-text uitk-type-300 uitk-type-bold uitk-text-default-theme'})
        counter3 = sum(1 for _ in inspect_hotel_names)
        hotel_rating = [rating.text for rating in inspect_hotel_rating]

        # Maximum number of hotels displayed: 10
        entries0 = min(counter0, 10)
        entries1 = min(counter1, 10)
        entries2 = min(counter2, 10)
        entries3 = min(counter3, 10)

        # No hotels then retry
        if entries0 == 0 or entries1 == 0 or entries2 == 0 or entries3 == 0:
            print(f"{chatbot_name}: Sorry, there are no hotels avaliable. Would you like to try again?")
            retry_hotel = input(f"{username}: ")
            # Intent matching for cancel, continue or quit
            intent1 = compare_intent(retry_hotel.lower(), intent_threshold)

            if ('cancellation' in intent1):
                print(f"{chatbot_name}: {username}, thanks for trying to book!")
                break

            if ('accept' in intent1):
                print(f"{chatbot_name}: Okay, we will choose a different place, my liege!")
                print("--------------------------------------------------")
            else:
                transaction_flag = False
        else:
            if not hotel_prices:
                print("No hotels found sir! Try again!")
                continue
            else:
                # Output all hotels up to max 10
                for i in range(entries0):
                    print(f"  {(i+1):02}. \'{hotel_names[i]}\' at {hotel_prices[i]} {hotel_nights[i]} - Rating: {hotel_rating[i]}")


            print(f"\n{chatbot_name}: Would you like to make a booking at one of these hotels? (Yes/No)")

            # Intent matching checking if user wants to make a booking
            while True:
                answer = input(f"{username}: ")
                intent = compare_intent(answer.lower(), intent_threshold)

                if answer.isdigit():
                    print(f"{chatbot_name}: Your answer shouldn't be a number!")
                elif answer == '':
                    print(f"{chatbot_name}: Your answer shouldn't be empty!")
                elif ('cancellation' in intent):
                    print(f"{chatbot_name}: {username}, thanks for trying to book!")
                    return
                elif ('decline' in intent):
                    print("--------------------------------------------------")
                    print(f"{chatbot_name}: Let's try again!")
                # If user similarity like 'accept' ID then simulate booking
                elif ('accept' in intent):
                    hotel_number_flag = True
                    while hotel_number_flag:
                        print(f"{chatbot_name}: Please enter the number of the hotel to confirm your booking.")
                        hotel_number = input(f"{username}: ")

                        if (not hotel_number.isdigit()):
                            print(f"{chatbot_name}: Sir, that isn't an option!")

                        #If valid number, break out of loop and confirm booking
                        elif (int(hotel_number) > 0 and int(hotel_number) < 11):
                            break

                        else:
                            print(f"{chatbot_name}: Sir, that isn't an option!")

                    # Print confirmation with hotel selected
                    # Add one to number as indexes greater, hotel numbers don't start at 0
                    hotel_number = int(hotel_number) - 1
                    print("---------------------------------------")
                    print(f"{chatbot_name}: You have selected {int(hotel_number)+1:02}. \'{hotel_names[int(hotel_number)]}\' at {hotel_prices[int(hotel_number)]} {hotel_nights[int(hotel_number)]} - Rating: {hotel_rating[int(hotel_number)]}")
                    print(f"{chatbot_name}: Congratulations! Your booking has been confirmed.")
                    print(f"{chatbot_name}: Please continue using me or make another transaction. For example: \"What is the time?\"")
                    hotel_number_flag = False
                    transaction_flag = False
                    return
                else:
                    print(f"{chatbot_name}: Sorry I did not understand that. Please answer again")
    return