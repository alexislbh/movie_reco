import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image 

imdb = pd.read_csv("./imdb_movie.csv")
imdb['original_language'] = pd.factorize(imdb.original_language)[0]

st.title("Movie Reco") 

ans = st.selectbox ('Votre film préféré', imdb.title, index=6040)
img_ans = imdb.poster_url[imdb.title==ans]
if pd.isna(img_ans.values[0]) == False:
  st.image(img_ans.values[0], width = 200)
else:
  st.image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 200)

#KNN
def knn_reco(ans):
  X = imdb[['isAdult', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western','original_language']]

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * 1.5
  x_scaled['startYear'] = x_scaled.startYear * 1.2
  x_scaled.iloc[:,5:] = x_scaled.iloc[:,5:] * 1.2
  x_scaled['averageRating'] = x_scaled.averageRating * 0.8
  x_scaled['original_language'] = x_scaled.original_language * 5

  distanceKNN = NearestNeighbors(n_neighbors=6).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.title == ans])

  newFilm = pd.DataFrame([imdb.iloc[predict[1][0][i],:] for i in range(6)],columns = imdb.columns) 
  
  return newFilm

  

newFilm = knn_reco(ans)
st.write(newFilm)

for num in range(1,6):
  if pd.isna(newFilm.poster_url.values[num]) == False:
    st.subheader(newFilm.title.values[num])
    st.image(newFilm.poster_url.values[num], width = 200)
  else:
    st.subheader(newFilm.title.values[num])
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 200)

st.image('http://img.omdbapi.com/?apikey=st.secrets["key"]&i=tt0052646, width = 200')
