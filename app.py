import pandas as pd
import numpy as np
import streamlit as st


st.title('Movie reco')

@st.cache
def load_data():
   imdb = pd.read_csv('Pilouliz-data/imdb_movie.csv')
   return imdb

df = load_data()
st.write(df)

