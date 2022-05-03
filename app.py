import pandas as pd
import streamlit as st

st.title('Movie reco')
  
DATA_URL = ('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.zip')

st.dataframe(DATA_URL)
