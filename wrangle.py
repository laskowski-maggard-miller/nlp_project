from acquire import json_to_df
from prepare import df_cleaner

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

def cat_wrangle(extra_words = [], exclude_words = []):
    df = json_to_df()
    df = df_cleaner(df, extra_words = extra_words, exclude_words = exclude_words)
    full_df = df.shape[0]

    # Remove all null values in the readme (60 total rows)
    df = df[~df.language.isnull()]
    null_count = full_df - df.shape[0]
    print(f'Removed {null_count} rows with empty Readmes.')

    # Create a column with length of cleaned readme, in words
    df['cleaned_length'] = df.cleaned.str.split(' ').str.len()

    # Remove all rows with cleaned readmes less than 10 words long
    df = df[df.cleaned_length > 9]
    print(f'Removed {full_df - df.shape[0] - null_count} rows with Readmes < 10 words long.')

    # Bucksets all languages into 3 most common + others
    df['language_group'] = np.where(df['language'] == 'Scala', 'Scala', np.where(df['language'] == 'Python', 'Python', np.where(df['language'] == 'JavaScript', 'JavaScript', 'Other')))

    # Create Dataframe to store original Readme, as well as specific language data, in case either are needed later
    # Then drop both columns
    df_languages = df[['readme_contents','language']]
    df = df.drop(columns = ['readme_contents','language'])

    # Splits
    train, validate, test = splitter(df, target = 'language_group')

    # Creates X and y versions of train, test and split
    # Note: We did not scale the numerical data (word count) as it was not necessary
    X_train = train.drop(columns = ['language_group'])
    y_train = train.language_group

    X_validate = validate.drop(columns = ['language_group'])
    y_validate = validate.language_group

    X_test = test.drop(columns = ['language_group'])
    y_test = test.language_group

    return X_train, y_train, X_validate, y_validate, X_test, y_test, df, df_languages

def splitter(df, target = 'None', train_split_1 = .8, train_split_2 = .7, random_state = 123):
    '''
    Splits a dataset into train, validate and test dataframes.
    Optional target, with default splits of 56% 'Train' (80% * 70%), 20% 'Test', 24% Validate (80% * 30%)
    Defailt random seed/state of 123
    '''
    if target == 'None':
        train, test = train_test_split(df, train_size = train_split_1, random_state = random_state)
        train, validate = train_test_split(train, train_size = train_split_2, random_state = random_state)
        print(f'Train = {train.shape[0]} rows ({100*(train_split_1*train_split_2):.1f}%) | Validate = {validate.shape[0]} rows ({100*(train_split_1*(1-train_split_2)):.1f}%) | Test = {test.shape[0]} rows ({100*(1-train_split_1):.1f}%)')
        print('You did not stratify.  If looking to stratify, ensure to add argument: "target = variable to stratify on".')
        return train, validate, test
    else: 
        train, test = train_test_split(df, train_size = train_split_1, random_state = random_state, stratify = df[target])
        train, validate = train_test_split(train, train_size = train_split_2, random_state = random_state, stratify = train[target])
        print(f'Train = {train.shape[0]} rows ({100*(train_split_1*train_split_2):.1f}%) | Validate = {validate.shape[0]} rows ({100*(train_split_1*(1-train_split_2)):.1f}%) | Test = {test.shape[0]} rows ({100*(1-train_split_1):.1f}%)')
        return train, validate, test
