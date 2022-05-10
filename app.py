import pandas as pd
import numpy as np
import streamlit as st
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image

st.set_page_config(
     page_title="Algo recomandation",
     page_icon="🦾",
     layout="wide",
     initial_sidebar_state="expanded"
)

st.button('label')

st.write(f'''
    <a target="_self" href="https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py" style="text-decoration: none;color:white">
        <button kind="primary" class="css-1q8dd3e edgvbvh9" style=text-align:center">
            Dataset  &  Dataviz
        </button>
    </a>
    ''',
    unsafe_allow_html=True
        )

st.title("Movie Reco") 

imdb_movie = pd.read_pickle('./imdb_movie.pkl')
imdb_original_language = pd.read_pickle('./imdb_original_language.pkl')
imdb = pd.merge(imdb_movie, imdb_original_language, how="left", on=["tconst"])

setting_name = ['Num Vote','Year','Genres','Rating','Region','Directors','Keyword']
settings =[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
#setting_algo = {'Num Vote':1.0,
#                'Year':1.0,
#                'Rating':1.0,
#                'Region':1.0,
#                'Genres':1.0,
#                'Directors':1.0,
#                'Keyword':1.0,
#                'Actors':1.0
#               }

with st.sidebar:
#if False:
  Actors = st.checkbox('Actors')
  Directors = st.checkbox('Directors')
  Genres = st.checkbox('Genres')
  Keyword = st.checkbox('Keyword')
  if Actors:
    imdb_actors = pd.read_pickle('./imdb_actors.pkl')
    imdb = pd.merge(imdb, imdb_actors, how="left", on=["tconst"])
    setting_name.append('Actors')
  else:
    if 'Actors' in setting_name:
      setting_name.remove('Actors')
  if Directors:
    imdb_directors = pd.read_pickle('./imdb_directors.pkl')
    imdb = pd.merge(imdb, imdb_directors, how="left", on=["tconst"])
  if Genres:
    imdb_genres = pd.read_pickle('./imdb_genres.pkl')
    imdb = pd.merge(imdb, imdb_genres, how="left", on=["tconst"])
  if Keyword:
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb, imdb_movie_keyword, how="left", on=["tconst"])


def get_OMDB(movieID):
  OMDB = requests.get('http://www.omdbapi.com/?i='+ movieID + '&apikey=' + st.secrets["key"]).json()
  return OMDB
  
cols = st.columns(len(settings))
for i in range(len(settings)):
  settings[i] = cols[i].number_input(setting_name[i],value=settings[i],step=0.1)
  cols[i].write(settings[i])
cols = st.columns(len(setting_algo))
#i=0
#for key, value in setting_algo.items():
#   cols[i].number_input(key,value=value,step=0.1)
#   i+=1

slider_val = st.slider('Choose your number of recomendation', 1, 15, value=5)
reco_val = slider_val + 1
ans = st.selectbox ('Votre film préféré', imdb.title, index=21301)

with st.sidebar:
  st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb.title[imdb.title==ans].values[0]), unsafe_allow_html=True)
  st.image(get_OMDB(imdb.tconst[imdb.title==ans].values[0])['Poster'], use_column_width = 'auto')
  cols1, cols2, cols3, cols4, cols5 = st.columns([1, 3, 1,3,1])
  cols2.metric(label="Rating", value=imdb.averageRating[imdb.title==ans].values[0])
  cols4.metric(label='Year', value=int(imdb.startYear[imdb.title==ans].values[0]))
  #st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb[imdb.title==ans].index[0]), unsafe_allow_html=True)


#KNN
def knn_reco(ans):
  global reco_val
  global settings
  global Actors
  global Directors
  global genres
  global keyword
  X = imdb.drop(['tconst','title','genres','original_language'], axis =1)

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * settings[0]
  x_scaled['startYear'] = x_scaled.startYear * settings[1]
  if Genres:
    x_scaled.loc[:,'Action':'Western'] = x_scaled.loc[:,'Action':'Western'] * settings[2]
    x_scaled['Drama'] = x_scaled.Drama * 0.5
  x_scaled['averageRating'] = x_scaled.averageRating * settings[3]
  x_scaled.loc[:,'ab':'zu'] = x_scaled.loc[:,'ab':'zu'] * settings[4]
  if Directors:
    x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] = x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] * settings[5]
  if Keyword:    
    x_scaled.loc[:,'woman director':'summer vacation'] = x_scaled.loc[:,'woman director':'summer vacation'] * settings[6]
  if Actors:
    x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] = x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] * settings[7]
  
  
  distanceKNN = NearestNeighbors(n_neighbors=reco_val).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.title == ans])
  
  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(reco_val)],columns = imdb.columns) 
  
  return newFilm

newFilm = knn_reco(ans)

Data_Debug = st.checkbox('Data Debug')
if Data_Debug :
  expander = st.expander("Data Debug")
  expander.write(newFilm)

step_range = sum([slider_val//5 if slider_val%5==0 else slider_val//5 +1])

for steps in range(step_range):
  next_line = steps * 5
  cols = st.columns(5)
  for num in range(1 + next_line,6 + next_line):
    if num == reco_val:
      break
    cols[(num-1) - next_line].markdown("<p style='text-align: center'><b>{}</b><font color='black'> - - - - </font><i>{}</i></p>".format(round(newFilm.averageRating.values[num],1), newFilm.startYear.values[num]), unsafe_allow_html=True)
    cols[(num-1) - next_line].image(get_OMDB(newFilm.tconst.values[num])['Poster'], use_column_width = 'auto')
    cols[(num-1) - next_line].markdown("<p style='text-align: center'>{}</p>".format(newFilm.title.values[num]), unsafe_allow_html=True)
