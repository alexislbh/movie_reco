import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image 

df = pd.read_csv("./imdb_movie.csv") 

st.title("Movie Reco") 

ans = st.selectbox ('Votre film préféré', df.title, index=6040)
img_ans = df.poster_url[df.title==ans]
if pd.isna(img_ans.values[0]) == False:
  st.image(img_ans.values[0], width = 200)
else:
  st.image('https://upload.wikimedia.org/wikipedia/commons/e/e6/Pas_d%27image_disponible.svg', width = 200)

#KNN
def knn_reco(ans)
  X = imdb[['isAdult', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western','original_language']]

  scale = StandardScaler().fit(X) 
  X_scaled = scale.transform(X)
  X_scaled = scale.transform(X)

  x_scaled = pd.DataFrame(X_scaled, columns=X.columns)

  x_scaled['numVotes'] = x_scaled.numVotes * 1.5
  x_scaled['startYear'] = x_scaled.startYear * 1.2
  x_scaled.iloc[:,5:] = x_scaled.iloc[:,5:] * 1.2
  x_scaled['averageRating'] = x_scaled.averageRating * 0.8
  x_scaled['original_language'] = x_scaled.original_language * 2

  distanceKNN = NearestNeighbors(n_neighbors=6).fit(X_scaled)

  predict = distanceKNN.kneighbors(X_scaled[imdb.title == ans)

  newFilm = pd.DataFrame(columns = imdb.columns) 

  for i in range(6):
    newFilm = newFilm.append(imdb.iloc[predict[1][0][i],:])
    #if i !=0 : print(np.array(newFilm.title)[i]) # Affiche que le nom des films
  return newFilm #Debug
                                            
st.write(knn_reco(ans))
