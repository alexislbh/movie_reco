import pandas as pd
import streamlit as st

st.title('Uber pickups in NYC')
  
imdb = pd.read_csv('imdb_movie.zip')

DATA_URL = ('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.zip')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
