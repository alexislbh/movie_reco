import pandas as pd
import numpy as np
import streamlit as st


df = pd.read_csv("./imdb_movie.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Hello world!")  # add a title
#st.write(df)  # visualize my dataframe in the Streamlit app

st.text_input('ecrire ici')

st.multiselect('choose columns', df.title)


