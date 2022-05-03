import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image 

img = Image.open("streamlit.png") 
  
st.image(img, width=200) 

df = pd.read_csv("./imdb_movie.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Movie Reco")  # add a title
#st.write(df)  # visualize my dataframe in the Streamlit app

#answ = st.multiselect('Votre film préféré', df.title)
ans = st.selectbox ('Votre film préféré', df.title, index=3623)

