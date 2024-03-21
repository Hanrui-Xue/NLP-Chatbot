import json
import random
import time
import timeit

from processing import string_processing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Computes similarity value
def compare_intent(query, intent_strength):
    training_query = []
    pattern_response = []

    # Processes the query, keeping stopwords
    processed_query = string_processing(query, False)
    # Set the query to be our TESTING data, stored as a tuple
    test_query = (processed_query, "")

    # Save the JSON object to a file and load, closes when done
    with open('data/intent.json') as f:
        data = json.load(f)
    # Iterates through intent file
    for row in data['intents']:
        # Assigns number tag to each pattern
        for i, j in enumerate(row['patterns']):
            # Assigns a random response to each pattern using their tag and store
            random_tagged = (row['id'], random.choice(row['responses']))
            # Append ID-response to array
            pattern_response.append(random_tagged)
            # Append all possible patterns to training set
            training_query.append(row['patterns'][i])

    # Calculates TF-IDF, vectorizes and assigns cosine similarity
    matrix = vectorize_cosine(training_query, test_query)
    # Copies array and collapses into one dimension
    flatten_matrix = matrix.flatten()

    #TEST SIMILARITY: print(max(flatten_matrix))
    # Compares similarity value to threshold, if less then return None (no intent match)
    if max(flatten_matrix) <= intent_strength:
        return (None, None)
    # Intent matches, finds most similar response, iterates over both lists, returns first element with 
    # corresponding index in list of max elements in flatten_matrix
    for index, pr in enumerate(pattern_response):
        if index in [index for index, value in enumerate(flatten_matrix) if value == max(flatten_matrix)]:
            return pr
            
# Calculates TF-IDF, vectorizes and assigns cosine similarity
def vectorize_cosine(training_query, test_query):
    # Can use countvectorizer + tfidf transformer here as well, tfidfvectorizer better
    # TF-IDF and vectorizes
    tfidf_vectorizer = TfidfVectorizer()
    # Scale the training data, TF-IDF vectorizes training_query
    training_vector = tfidf_vectorizer.fit_transform(training_query)

    # Convert data to vectorize the query (testing data) with TF-IDF
    test_vector = tfidf_vectorizer.transform(test_query)

    # Returns the cosine similarity value between test_vector and training_vector
    return linear_kernel(test_vector, training_vector)[0]


