import json
import requests

from bs4 import BeautifulSoup
from intent_matching import vectorize_cosine

from processing import string_processing

# Answers questions in the COMP3074-CW1-Dataset.csv using intent matching
def question_answering(query, threshold):

    training_query = []

    # Processes user input and removes stopwords
    processed_query = string_processing(query, True)

    # Creates tuple with pre-processed user input
    test_query = (processed_query, "")

    # Save the JSON object to a file and load, closes when done
    with open('output/Dataset.json') as f:
        data = json.load(f)

    # Process all rows for column Question and remove stop words and append to training array
    for row in data:
        processed_query = string_processing(row['Question'], True)
        training_query.append(processed_query)

    # Uses function in intent_matching to apply TF-IDF, vectorize and calculate cosine similarity
    cosine_matrix = vectorize_cosine(training_query, test_query)

    # Intent matches, finds most similar response, iterates over both lists, returns first element with corresponding
    # index in list of max elements in flatten_matrix
    max_value_index = [index for index, value in enumerate(cosine_matrix.flatten()) if value == max(cosine_matrix.flatten())]

    # Compares similarity value to threshold, if less then web scrape google for an answer
    if max(cosine_matrix.flatten()) <= threshold:
        return google_result if (google_result := google_search(query)) else "I can't find what you are looking for, my liege. Try something else."

    # Save the JSON object to a file and load, closes when done
    with open('output/Dataset.json') as d:
        data = json.load(d)

    # Obtains the row in column answer that matches the index 
    answers_list = [row['Answer'] for index, row in enumerate(data) if index in max_value_index]

    # Joins list as a whole string, removes commas
    return " ".join(answers_list)

# REFERENCE HELP: Real Python (2022) Beautiful soup: Build a web scraper with python, 
# Real Python. Real Python. Available at: https://realpython.com/beautiful-soup-web-scraper-python/. 

# Web scrapes Google using BeautifulSoup
def google_search(search_parameter):
    # Defines web browser and OS that is used to make the request
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    # Defines google URl, adds user input to end of URL
    url = f"https://www.google.com/search?q={search_parameter}"
    # Sends a get request to Google 
    req_result = requests.get(url, headers=headers)
    # Parse HTML content with Python's built-in HTML parser and create object from web contents text req_results
    soup = BeautifulSoup(req_result.text, "html.parser")

    # Declare and initialises result
    # Specifies HTML element to search for and selects else returns None
    if result := soup.select_one('div.kno-rdesc > span'):
        # If selected keep it on one line for output and return result
        processed_result = result.text.replace("\n", " ")
        return f"(Sourced from Google) {processed_result}."
    else:
        return None