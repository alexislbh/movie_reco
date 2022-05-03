import pandas as pd
import streamlit as st

st.title('Movie reco')

#imdb = pd.read_csv('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.csv')

#st.dataframe(imdb)

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
