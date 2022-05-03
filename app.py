import pandas as pd
import streamlit as st

st.title('Movie reco')

imdb = pd.read_csv('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.zip')

st.dataframe(imdb)
