import pandas as pd
import numpy as np
import streamlit as st
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image

#st.button('Select',on_click=('https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py'))
#st.markdown('Essayez notre [algorithme de recommandation](https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py)')

#st.write(f'''
#    <a target="_self" href="https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py">
#        <button>
#            Nos recommandations
#        </button>
#    </a>
#    ''',
#    unsafe_allow_html=True
#        )

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("Movie Reco") 

imdb = pd.read_pickle('./imdb_movie.pkl')

#with st.sidebar:
if False:
  Rien = st.checkbox('Base')
  Real = st.checkbox('Réalisateur')
  Keyword = st.checkbox('Mots clés')
  if Rien:
    imdb = imdb.drop(columns=imdb.iloc[:,8:30].columns)
  elif Real:
    imdb = imdb
  elif Keyword:
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb, imdb_movie_keyword, how="inner", on=["tconst"])


with st.sidebar:
#if False:
  genre = st.radio("Algo fonctionnement", ('Tout', 'real', 'Keyword', 'Rien'))
  if genre == 'Tout':
    imdb_movie = pd.read_pickle('./imdb_movie.pkl')
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb_movie, imdb_movie_keyword, how="inner", on=["tconst"])
  elif genre == 'real':
    imdb = pd.read_pickle('./imdb_movie.pkl')
  elif genre == 'Keyword':
    imdb_movie = pd.read_pickle('./imdb_movie.pkl')
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb_movie, imdb_movie_keyword, how="inner", on=["tconst"])
    imdb = imdb.drop(columns=imdb.iloc[:,8:30].columns)
  elif genre == 'Rien':
    imdb_movie = pd.read_pickle('./imdb_movie.pkl')
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb_movie, imdb_movie_keyword, how="inner", on=["tconst"])
    imdb = imdb.drop(columns=imdb.iloc[:,8:].columns)

setting_name = ['Num Vote','Year','Genre','Rating','Region','Réalistaeur','Keyword']
settings =[1.0,1.0,1.0,1.0,1.0,1.0,1.0]

def get_OMDB(movieID):
  OMDB = requests.get('http://www.omdbapi.com/?i='+ movieID + '&apikey=' + st.secrets["key"]).json()
  return OMDB
  
cols = st.columns(len(settings))
for i in range(len(settings)):
  settings[i] = cols[i].number_input(setting_name[i],value=settings[i],step=0.1)
  cols[i].write(settings[i])

slider_val = st.slider('Choose your number of recomendation', 1, 15, value=5)
reco_val = slider_val + 1
ans = st.selectbox ('Votre film préféré', imdb.title, index=6040)

with st.sidebar:
  st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb.title[imdb.title==ans].values[0]), unsafe_allow_html=True)
  st.image(get_OMDB(imdb.tconst[imdb.title==ans].values[0])['Poster'], use_column_width = 'auto')
  cols1, cols2, cols3, cols4, cols5 = st.columns([1, 3, 1,3,1])
  cols2.metric(label="Rating", value=imdb.averageRating[imdb.title==ans].values[0])
  cols4.metric(label='Year', value=int(imdb.startYear[imdb.title==ans].values[0]))


#KNN
def knn_reco(ans):
  global reco_val
  global settings
  X = imdb.drop(['tconst','originalTitle','title'], axis =1)

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * settings[0]
  x_scaled['startYear'] = x_scaled.startYear * settings[1]
  x_scaled.iloc[:,8:30] = x_scaled.iloc[:,8:30] * settings[2]
  x_scaled['averageRating'] = x_scaled.averageRating * settings[3]
  x_scaled.iloc[:,30:96] = x_scaled.iloc[:,30:96] * settings[4]
  x_scaled.iloc[:,96:817] = x_scaled.iloc[:,96:817] * settings[5]
  x_scaled.iloc[:,817:] = x_scaled.iloc[:,817:] * settings[6]
  #x_scaled['Drama'] = x_scaled.numVotes * 0.2
  
  distanceKNN = NearestNeighbors(n_neighbors=reco_val).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.title == ans])
  
  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(reco_val)],columns = imdb.columns) 
  
  return newFilm

newFilm = knn_reco(ans)

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
    if cols[(num-1) - next_line].button('Select'):
      ans = newFilm.title.values[num]
