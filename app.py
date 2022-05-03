import pandas as pd
import numpy as np
import streamlit as st


st.title('Movie reco')

@st.cache
def load_data():
   imdb = pd.read_csv('https://drive.google.com/file/d/1-u3h1PuOtF1xxh1po3N_wUhpU3UeUZ-B/view?usp=sharing')
   return imdb

df = load_data()
st.write(df)

