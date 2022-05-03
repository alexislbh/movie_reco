import pandas as pd
import streamlit as st

st.title('Movie reco')
  
DATA_URL = ('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.zip')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data
