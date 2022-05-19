import pandas as pd
import numpy as np
import streamlit as st
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image

### Page Setup
st.set_page_config(
     page_title="Recommandation de films",
     page_icon="🦾",
     layout="wide",
     initial_sidebar_state="expanded"
)


#st.write(f'''
#    <a target="_self" href="https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py" style="text-decoration: none;color:white">
#        <button class="css-1q8dd3e edgvbvh9 button" style=text-align:center">
#            Data Analysis
#        </button>
#    </a>
#    ''',
#    unsafe_allow_html=True
#        )
#st.button('')



st.title("Recommandation de films")

st.subheader('Option : Ajuster les poids')

### Datasets
imdb_movie = pd.read_pickle('./imdb_movie.pkl')
imdb_original_language = pd.read_pickle('./imdb_original_language.pkl')
imdb = pd.merge(imdb_movie, imdb_original_language, how="left", on=["tconst"])

datasets_name = {'Actors': pd.read_pickle('./imdb_actors.pkl'),
                'Directors':pd.read_pickle('./imdb_directors.pkl'),
                'Genres': pd.read_pickle('./imdb_genres.pkl'),
                'Keyword': pd.read_pickle('./imdb_movie_keyword.pkl')}

### Fonction activation dataset
def get_dataset(name):
  global imdb
  global setting_name
  global settings
  global setting_algo
  global datasets_name
  imdb = pd.merge(imdb, datasets_name[name], how="left", on=["tconst"])
  setting_name.append(name)
  settings.append(setting_algo[name])

### Fonction désactivation dataset
def drop_dataset(name):
  global setting_name
  global settings
  global setting_algo
  if name in setting_name:
    setting_name.remove(name)
    settings.remove(setting_algo[name])


### réglages des poids par defauts
setting_name = ['Num Vote','Year','Rating','Region']
settings =[1.7,1.0,1.0,0.7]
setting_algo = {'Num Vote':1.7,
                'Year':1.0,
                'Rating':1.0,
                'Region':0.7,
                'Genres':1.0,
                'Directors':1.0,
                'Keyword':1.0,
                'Actors':1.0
               }

### Chargement de datasets suplémentaires
with st.sidebar:
  Genres = st.checkbox('Genres',value=True)
  Actors = st.checkbox('Acteurs')
  Directors = st.checkbox('Réalisateurs')
  Keyword = st.checkbox('Mots-clés')
  
  if Genres:
    get_dataset('Genres')
  else:
    drop_dataset('Genres')
  if Actors:
    get_dataset('Actors')
  else:
    drop_dataset('Actors')
  if Directors:
    get_dataset('Directors')
  else:
    drop_dataset('Directors')
  if Keyword:
    get_dataset('Keyword')
  else:
    drop_dataset('Keyword')

### Récuperer les informations depuis OMDB API
def get_OMDB(movieID):
  OMDB = requests.get('http://www.omdbapi.com/?i='+ movieID + '&apikey=' + st.secrets["key"]).json()
  return OMDB

### Regales de la gestion des poids utilisateurs 'Front End'
cols = st.columns(len(setting_name))
for i in range(len(setting_name)):
   settings[i] = cols[i].number_input(setting_name[i],value=settings[i],step=0.3)
 # cols[i].write(settings[i])

### Slider choix du nombre de recommendation
slider_val = st.slider('Choisissez le nombre de films à recommander', 1, 15, value=5)
reco_val = slider_val + 1
ans = st.selectbox ('Votre film préféré', imdb.titleView, index=21301)
#st.write(ans)

### Présentation du film choisit
with st.sidebar:
  st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb.title[imdb.titleView==ans].values[0]), unsafe_allow_html=True)
  st.image(get_OMDB(imdb.tconst[imdb.titleView==ans].values[0])['Poster'], use_column_width = 'auto')
  cols1, cols2, cols3, cols4, cols5 = st.columns([1, 3, 1,3,1])
  cols2.metric(label="Rating", value=imdb.averageRating[imdb.titleView==ans].values[0])
  cols4.metric(label='Year', value=int(imdb.startYear[imdb.titleView==ans].values[0]))


### KNN - K-nearest neighbors - Algorithme des K plus proches voisins - Déclaré dans une fonction
def knn_reco(ans):
  ### Variables exterieures à la fonction
  global reco_val
  global settings
  global Actors
  global Directors
  global genres
  global keyword
     
  X = imdb.drop(['tconst','title','genres','original_language','titleView'], axis =1)

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)
  
  ### Réglage des poids directement dans l'algo
  x_scaled['numVotes'] = x_scaled.numVotes * settings[0]
  x_scaled['startYear'] = x_scaled.startYear * settings[1]
  if Genres:
    x_scaled.loc[:,'Action':'Western'] = x_scaled.loc[:,'Action':'Western'] * settings[setting_name.index('Genres')]
    x_scaled['Drama'] = x_scaled.Drama * 0.3
    x_scaled['Animation'] = x_scaled.Animation * 2
  x_scaled['averageRating'] = x_scaled.averageRating * settings[2]
  x_scaled.loc[:,'ab':'zu'] = x_scaled.loc[:,'ab':'zu'] * settings[3]
  if Directors:
    x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] = x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] * settings[setting_name.index('Directors')]
  if Keyword:    
    x_scaled.loc[:,'woman director':'dirty cop'] = x_scaled.loc[:,'woman director':'dirty cop'] * settings[setting_name.index('Keyword')]
  if Actors:
    x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] = x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] * settings[setting_name.index('Actors')]
  
  
  distanceKNN = NearestNeighbors(n_neighbors=reco_val).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.titleView == ans])
  
  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(reco_val)],columns = imdb.columns) 
  
  return newFilm

newFilm = knn_reco(ans)

### Afficher du Datafraame 'newFilm pour vérifier des infos
#Data_Debug = st.checkbox('Informations brutes')
#if Data_Debug :
#  expander = st.expander("Informations brutes")
#  expander.write(newFilm)

### ------ Affichae des réponses de recomendation ------ ###

##Nombre de lignes à afficher en fonction du choix de reco (5 par lignes)
line_range = sum([slider_val//5 if slider_val%5==0 else slider_val//5 +1])

for lines in range(line_range):
  next_line = lines * 5
  cols = st.columns(5)
  for num in range(1 + next_line,6 + next_line):
    if num == reco_val:
      break
    cols[(num-1) - next_line].markdown("<p style='text-align: center'><b>{}</b><font color='black'> - - - - </font><i>{}</i></p>".format(round(newFilm.averageRating.values[num],1), newFilm.startYear.values[num]), unsafe_allow_html=True)
    cols[(num-1) - next_line].image(get_OMDB(newFilm.tconst.values[num])['Poster'], use_column_width = 'auto')
    cols[(num-1) - next_line].markdown("<p style='text-align: center'>{}</p>".format(newFilm.title.values[num]), unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;font-size:18px;'> JAO Data : Alexis Le Bihan, Julien Reppert, Oscar Arnoux</h1>", unsafe_allow_html=True)
