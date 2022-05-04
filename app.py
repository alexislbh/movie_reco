import pandas as pd
import numpy as np
import streamlit as st
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

imdb = pd.read_csv("./imdb_movie.csv")
imdb['original_language'] = pd.factorize(imdb.original_language)[0]

st.title("Movie Reco") 

setting_name = ['Num Vote','Year','Genre','Rating','Region']
settings =[1.0,1.0,1.0,1.0,3.0]

cols = st.columns(len(settings))
for i in range(len(settings)):
  settings[i] = cols[i].number_input(setting_name[i],value=settings[i],step=0.1)
  cols[i].write(settings[i])

slider_val = st.slider('Choose your number of recomendation', 1, 15, value=5)
reco_val = slider_val + 1
ans = st.selectbox ('Votre film préféré', imdb.title, index=6040)

with st.sidebar:
  st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb.title[imdb.title==ans].values[0]), unsafe_allow_html=True)
  img_ans = imdb.poster_url[imdb.title==ans]
  if pd.isna(img_ans.values[0]) == False:
    st.image(img_ans.values[0], use_column_width=True)
  else:
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 200)
  cols1, cols2, cols3, cols4, cols5 = st.columns([1, 3, 1,3,1])
  cols2.metric(label="Rating", value=imdb.averageRating[imdb.title==ans].values[0])
  cols4.metric(label='Year', value=int(imdb.startYear[imdb.title==ans].values[0]))
  

#KNN
def knn_reco(ans):
  global reco_val
  global settings
  X = imdb[['isAdult', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western','original_language']]

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * settings[0]
  x_scaled['startYear'] = x_scaled.startYear * settings[1]
  x_scaled.iloc[:,5:] = x_scaled.iloc[:,5:] * settings[2]
  x_scaled['averageRating'] = x_scaled.averageRating * settings[3]
  x_scaled['original_language'] = x_scaled.original_language * settings[4]
  
  distanceKNN = NearestNeighbors(n_neighbors=reco_val).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.title == ans])
  
  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(reco_val)],columns = imdb.columns) 
  
  return newFilm

newFilm = knn_reco(ans)

expander = st.expander("Data")
expander.write(newFilm)

step_range = sum([slider_val//5 if slider_val%5==0 else slider_val//5 +1])


for steps in range(step_range):
  next_line = steps * 5
  cols = st.columns(5)
  for num in range(1 + next_line,6 + next_line):
    if num == reco_val:
      break
    if pd.isna(newFilm.poster_url.values[num]) == False:
      cols[(num-1) - next_line].image(newFilm.poster_url.values[num], width = 150)
    else:
      cols[(num-1) - next_line].image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 150)
    cols[(num-1) - next_line].markdown("<p style='text-align: center'>{}</p>".format(newFilm.title.values[num]), unsafe_allow_html=True)
    cols[(num-1) - next_line].markdown("<p style='text-align: center'><b>{}</b><font color='black'> - - - - </font><i>{}</i></p>".format(newFilm.averageRating.values[num], newFilm.startYear.values[num]), unsafe_allow_html=True)
API_KEY = st.secrets["key"]
movieID = 'tt1285016'
OMDB = requests.get('http://www.omdbapi.com/?i='+ movieID + '&apikey=' + API_KEY).json()
st.write(OMDB)
st.write(OMDB['Poster'])
st.image(OMDB['Poster'])
