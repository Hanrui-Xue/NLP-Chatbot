import nltk
import re
import string
import json
import timeit
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Processes the Excel dataset supplied 
def dataset_processing():
    # Read the CSV file and convert it to a Pandas DataFrame
    df = pd.read_csv('data/COMP3074-CW1-Dataset.csv')

    # Drop rows with all missing values
    df = df.dropna(how="all")

    # Drop the 'QuestionID' and 'Document' columns
    df = df.drop(['QuestionID', 'Document'], axis=1)

    # Convert the DataFrame to a JSON object
    dataset_json = json.loads(df.to_json(orient='records'))

    # Save the JSON object to a file, closes when done
    with open('output/Dataset.json', 'w') as file_out:
        #Convert object to JSON and store info into file
        json.dump(dataset_json, file_out)


# function for language pre processing (tokenizing, lemmatizing etc)
# removes stopwords only for cases when needed, returns a processed string
def string_processing(query, remove_stopwordflag):
    #removing punctuations and lowercasing
    punct_query = query.translate(str.maketrans('', '', string.punctuation)).lower().strip()

    # Removing URLs with re standard python library (security)
    url_query = re.sub(r'http\S+', '', punct_query)

    # Tokenize with NLTK library
    tokenized_query = word_tokenize(url_query)

    # Removing stopwords if necessary
    if (remove_stopwordflag):
        english_stopwords = stopwords.words('english')
        tokenized_query = [word for word in tokenized_query if word not in english_stopwords]

    # Categorizes the tokens in text as n, v, adj, adv, etc.
    tokenized_query = nltk.pos_tag(tokenized_query)

    return token_lemma(tokenized_query)


# Tokenizes and lemmatizes query
def token_lemma(tokenized_query):

    processed_query = ''
    #Tokenization + Lemmatization
    lemmatizer = WordNetLemmatizer()

    # Maps tags to tokens in text
    posmap = {
        'ADJ': 'J',
        'ADV': 'R',
        'NOUN': 'N',
        'VERB': 'V'
    }

    # Loops through tokens in query
    for token in tokenized_query:
        # Assigns variables to first and second elements
        word = token[0]
        tag = token[1]

        # Checks if the tag is ADJ, ADV, NOUN, VERB (posmap)
        if tag in posmap:
            # Lemmatizes word according to word category
            tokens = lemmatizer.lemmatize(word, posmap[tag])
        else:
            # Lemmatizes word 
            tokens = lemmatizer.lemmatize(word)
        
        # Appends each lemmatized token to query and returns
        processed_query+=tokens
        processed_query+=' '

    return processed_query

