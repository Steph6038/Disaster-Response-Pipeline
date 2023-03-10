# import libraries and
import numpy as np
import pandas as pd
import sys
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    INPUT:
    database_filepath 
    
    OUTPUT:
    X - messages (input variable) 
    y - categories of the messages (output variable)
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = categories.merge(messages, on = 'id')
    return df


def clean_data(df):
   """
    INPUT:
    raw dataframe 
    
    OUTPUT:
    cleaned data frame with relevant information
    """
# create a dataframe of the 36 individual category columns
    categories = df.categories.str.split(pat=';', expand = True)
# select the first row of the categories dataframe
    row = categories.iloc[0]
#extract a list of new column names for categories.
    category_colnames = row.apply(lambda x:x[:-2])
# rename the columns of `categories`
    categories.columns = category_colnames
#Convert category values to just numbers 0 or 1
    for column in categories:
    # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
    # convert column from string to numeric
        categories[column] = categories[column].astype(np.int)
        
 # drop the original categories column from `df`
    df = df.drop(['categories', 'genre'] , axis=1)
# concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis =1)
# drop duplicates
    df = df.drop_duplicates()
#replacing 2 with 1 in related category   
    df.related.replace(2,1,inplace=True)
    print(column)
    print(categories[column].value_counts())
    return df
   


def save_data(df, database_filename):
    """
    w save the data into the selected datbase to refrence later.
    """
   engine = create_engine('sqlite:///'+ database_filename)
   df.to_sql('DisasterResponse', engine, if_exists='replace',index=False)
   df.dtypes 


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()