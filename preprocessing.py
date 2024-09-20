import gzip
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import torch

def open_to_df(file):
    '''
    Function to convert json to pandas dataframe
    '''
    data = []
    with gzip.open(file) as f:
        for l in f:
            data.append(json.loads(l.strip()))
    df = pd.DataFrame.from_dict(data)
    return df

def preprocess_data():
    # Load the metadata
    metadata = open_to_df('meta_Appliances.json.gz')
    select_item_col = ['asin', 'title', 'brand']
    itemdata = metadata[select_item_col].copy()

    # Load the user ratings
    userrating = open_to_df('Appliances.json.gz')
    userrating = userrating.iloc[35:, :]  # Remove erroneous data

    # Prepare the userdata
    select_userreview_col = ['reviewerID', 'asin', 'overall', 'unixReviewTime', 'reviewText']
    userdata = userrating[select_userreview_col].copy()

    # Merge item and user data
    cdata = pd.merge(userdata, itemdata, on='asin', how='inner')

    # Removing duplicate review records
    cdata['composite_key'] = cdata['reviewerID'].astype(str) + '_' + cdata['asin'].astype(str) + '_' + cdata['unixReviewTime'].astype(str)
    cdata = cdata.drop_duplicates(subset='composite_key')
    cdata = cdata.drop(columns='composite_key')

    # Fill missing values
    cdata = cdata.dropna(subset=['reviewText'])

    # Label encoding for user IDs
    label_encoder = LabelEncoder()
    cdata['reviewerID'] = label_encoder.fit_transform(cdata['reviewerID'])

    # Prepare item ID mapping
    itemnum_2_itemid = list(cdata['asin'].unique())
    itemnum_2_itemid.sort()
    itemid_2_itemnum = {c: i for i, c in enumerate(itemnum_2_itemid)}
    cdata['asin_id'] = cdata['asin'].apply(lambda x: itemid_2_itemnum[x])

    # Save the preprocessed data to a file
    cdata.to_csv('preprocessed_data.csv', index=False)
    return cdata

def load_preprocessed_data():
    return pd.read_csv('preprocessed_data.csv')

preprocess_data()
print(load_preprocessed_data().head())