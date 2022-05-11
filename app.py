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


st.write(f'''
    <a target="_self" href="https://share.streamlit.io/oscararnoux8/projet2_wcs/main/project2_viz.py" style="text-decoration: none;color:white">
        <button class="css-1q8dd3e edgvbvh9 button" style=text-align:center">
            Data Analysis
        </button>
    </a>
    ''',
    unsafe_allow_html=True
        )

st.title("Movie Reco")

imdb_movie = pd.read_pickle('./imdb_movie.pkl')
imdb_original_language = pd.read_pickle('./imdb_original_language.pkl')
imdb = pd.merge(imdb_movie, imdb_original_language, how="left", on=["tconst"])

avis_w = {'Très peu':0.3,'peu':0.7,'Neutre':1.0,'moyen':1.3,'beaucoup':1.7}
setting_name = ['Num Vote','Year','Rating','Region']
settings =[1.7,1.0,1.0,0.7]
setting_algo = {'Num Vote':4,
                'Year':2,
                'Rating':1,
                'Region':2,
                'Genres':2,
                'Directors':2,
                'Keyword':1,
                'Actors':2
               }
st.table(imdb.iloc[:,:10].head())

with st.sidebar:
  Genres = st.checkbox('Genres',value=True)
  Actors = st.checkbox('Actors')
  Directors = st.checkbox('Directors')
  Keyword = st.checkbox('Keyword')
     
  #def set_algo(set)
  #   if Actors:
  #  imdb_actors = pd.read_pickle('./imdb_actors.pkl')
  #  imdb = pd.merge(imdb, imdb_actors, how="left", on=["tconst"])
  #  setting_name.append('Actors')
  #  settings.append(setting_algo['Actors'])
  #else:
  #  if 'Actors' in setting_name:
  #    setting_name.remove('Actors')
  #    settings.remove(setting_algo['Actors'])

  if Actors:
    imdb_actors = pd.read_pickle('./imdb_actors.pkl')
    imdb = pd.merge(imdb, imdb_actors, how="left", on=["tconst"])
    setting_name.append('Actors')
    settings.append(setting_algo['Actors'])
  else:
    if 'Actors' in setting_name:
      setting_name.remove('Actors')
      settings.remove(setting_algo['Actors'])
  if Directors:
    imdb_directors = pd.read_pickle('./imdb_directors.pkl')
    imdb = pd.merge(imdb, imdb_directors, how="left", on=["tconst"])
    setting_name.append('Directors')
    settings.append(setting_algo['Directors'])
  else:
    if 'Directors' in setting_name:
      setting_name.remove('Directors')
      settings.remove(setting_algo['Directors'])
  if Genres:
    imdb_genres = pd.read_pickle('./imdb_genres.pkl')
    imdb = pd.merge(imdb, imdb_genres, how="left", on=["tconst"])
    setting_name.append('Genres')
    settings.append(setting_algo['Genres'])
  else:
    if 'Genres' in setting_name:
      setting_name.remove('Genres')
      settings.remove(setting_algo['Genres'])
  if Keyword:
    imdb_movie_keyword = pd.read_pickle('./imdb_movie_keyword.pkl')
    imdb = pd.merge(imdb, imdb_movie_keyword, how="left", on=["tconst"])
    setting_name.append('Keyword')
    settings.append(setting_algo['Keyword'])
  else:
    if 'Keyword' in setting_name:
      setting_name.remove('Keyword')
      settings.remove(setting_algo['Keyword'])


def get_OMDB(movieID):
  OMDB = requests.get('http://www.omdbapi.com/?i='+ movieID + '&apikey=' + st.secrets["key"]).json()
  return OMDB

cols = st.columns(len(setting_name))
for i in range(len(setting_name)):
  key = cols[i].selectbox(setting_name[i],avis_w.keys())
  settings[i] = avis_w[key] 
  #settings[i] = cols[i].number_input(setting_name[i],value=settings[i],step=0.1)
  cols[i].write(settings[i])

slider_val = st.slider('Choose your number of recomendation', 1, 15, value=5)
reco_val = slider_val + 1
ans = st.selectbox ('Votre film préféré', imdb.search, index=21301)
#st.write(ans)

with st.sidebar:
  st.markdown("<h2 style='text-align: center'>{}</h2>".format(imdb.title[imdb.search==ans].values[0]), unsafe_allow_html=True)
  st.image(get_OMDB(imdb.tconst[imdb.search==ans].values[0])['Poster'], use_column_width = 'auto')
  cols1, cols2, cols3, cols4, cols5 = st.columns([1, 3, 1,3,1])
  cols2.metric(label="Rating", value=imdb.averageRating[imdb.search==ans].values[0])
  cols4.metric(label='Year', value=int(imdb.startYear[imdb.search==ans].values[0]))


#KNN
def knn_reco(ans):
  global reco_val
  global settings
  global Actors
  global Directors
  global genres
  global keyword
  X = imdb.drop(['tconst','title','genres','original_language','search'], axis =1)

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * settings[0]
  x_scaled['startYear'] = x_scaled.startYear * settings[1]
  if Genres:
    x_scaled.loc[:,'Action':'Western'] = x_scaled.loc[:,'Action':'Western'] * settings[setting_name.index('Genres')]
    x_scaled['Drama'] = x_scaled.Drama * 0
    x_scaled['Drama'] = x_scaled.Animation * 2
  x_scaled['averageRating'] = x_scaled.averageRating * settings[2]
  x_scaled.loc[:,'ab':'zu'] = x_scaled.loc[:,'ab':'zu'] * settings[3]
  if Directors:
    x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] = x_scaled.loc[:,'Abbas Kiarostami':'Éric Rohmer'] * settings[setting_name.index('Directors')]
  if Keyword:    
    x_scaled.loc[:,'woman director':'dirty cop'] = x_scaled.loc[:,'woman director':'dirty cop'] * settings[setting_name.index('Keyword')]
  if Actors:
    x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] = x_scaled.loc[:,'Aaron Eckhart':'Zac Efron'] * settings[setting_name.index('Actors')]
  
  
  distanceKNN = NearestNeighbors(n_neighbors=reco_val).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.search == ans])
  
  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(reco_val)],columns = imdb.columns) 
  
  return newFilm

newFilm = knn_reco(ans)

#Data_Debug = st.checkbox('Data Debug')
#if Data_Debug :
#  expander = st.expander("Data Debug")
#  expander.write(newFilm)

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
