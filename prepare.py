import unicodedata
import re
import json

from bs4 import BeautifulSoup as bs

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

def scrubber(string):
    '''
    This function takes the data from our github repo acquire script and does an initial 'scrubbing", delimiting on spaces and then:
    - Removing all newlines
    - Removing urls
    - Removing all words greater than 14 characters (5 stds above the mean) - captures random code that sneaks through
    '''
    soup = bs(string, 'lxml').text
    
    split_soup = soup.split(' ')
    word_list = []

    for word in split_soup:
        if re.search(r"\n", word):
            continue
        if re.match(r'https:', word):
            continue
        if len(word) > 14:
            continue
        else:
            word_list.append(word)

    scrubbed = ' '.join(word_list)

    return scrubbed


def basic_clean(string):
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    return string

def tokenize(string):
    tokenizer = ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str=True)

    return string

def stem(string):
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string = ' '.join(stems)

    return string

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    Takes in a string and optional lists of stopwords to add and remove from the string, and returns the string without stopwords
    '''
    stopword_list = stopwords.words('english')
    # Remove stopwords to remove
    for word in exclude_words:
        stopword_list.remove(word)
    # Adds additional stopwords
    for word in extra_words:
        stopword_list.append(word)
    words = string.split(' ')
    filtered_words = [w for w in words if w not in stopword_list]
    #print('Removed {} stopwords'.format(len(words) - len(filtered_words)))

    stopwordless_string = ' '.join(filtered_words)

    return stopwordless_string

def remove_smalls(string):
    words = string.split(' ')
    large_words = [w for w in words if len(w) > 2]
    string = ' '.join(large_words)
    return string

def full_clean(string, extra_words = [], exclude_words = [], stem_or_lemma = 'lemma'):
    '''
    Function combines all NLP cleaning steps:
    1. Basic clean makes it lower case, removes non-unicode and special characters
    2. Tokenize
    3. Stem or Lemmatized based on parameter input - default is lemmatize
    4. 
    '''
    string = scrubber(string)
    string = basic_clean(string)
    string = tokenize(string)
    if stem_or_lemma == 'lemma':
        string = lemmatize(string)
    else:
        string = stem(string)
    string = remove_stopwords(string, extra_words, exclude_words)
    cleaned_string = remove_smalls(string)

    return cleaned_string   

def df_cleaner(df, extra_words = [], exclude_words = []):
    df_holder = [] 

    for rows in df.index:
        row = {}
        repo = df.iloc[rows][0]
        language = df.iloc[rows][1]
        readme_contents = df.iloc[rows][2]
        
        row['repo'] = repo
        row['language'] = language
        row['readme_contents'] = readme_contents
        
        row['cleaned'] = full_clean(readme_contents,extra_words,exclude_words)
        
        df_holder.append(row)
    df_cleaned = pd.DataFrame(df_holder)

    return df_cleaned