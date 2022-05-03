import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image 

df = pd.read_csv("./imdb_movie.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Movie Reco")  # add a title
#st.write(df)  # visualize my dataframe in the Streamlit app


ans = st.selectbox ('Votre film préféré', df.title, index=6040)
img_ans = df.poster_url[df.title==ans]
st.image(img_ans.values[0], width = 400)
st.image("https://www.themoviedb.org/t/p/original/63Ol9NX5E1OEsH7CHivNEvJMdky.jpg", width=200)


