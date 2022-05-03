import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image 

df = pd.read_csv("./imdb_movie.csv") 

st.title("Movie Reco") 

ans = st.selectbox ('Votre film préféré', df.title, index=6040)
img_ans = df.poster_url[df.title==ans]
#if pd.isna(img_ans) == True:
st.image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 200)
#else:
st.image(img_ans.value[0], width = 200)
  


