import pandas as pd
import streamlit as st

st.title('Movie reco')

#imdb = pd.read_csv('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.csv')

#st.dataframe(imdb)

df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(df)
