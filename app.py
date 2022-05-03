import pandas as pd
import streamlit as st

st.title('Movie reco')
  
DATA_URL = ('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.zip')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data
  
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
