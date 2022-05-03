import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


st.title('Movie reco')

imdb = pd.read_csv('https://github.com/Pilouliz/movie_reco/blob/main/imdb_movie.csv')

#st.dataframe(imdb)

st.title('Uber pickups in NYC')

X = imdb[['isAdult', 'startYear', 'runtimeMinutes',
       'averageRating', 'numVotes', 'Action', 'Adventure',
       'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western','original_language']]

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

try:
    predict = distanceKNN.kneighbors(X_scaled[imdb.title.str.lower() == input().lower()]) #Mettre le input en regex
    stop = 0
except ValueError:
    print("Le film n'est pas dans la séléction.")
    stop = 1

newFilm = pd.DataFrame(columns = imdb.columns) 

for i in range(6):
    if stop == 1: break
    newFilm = newFilm.append(imdb.iloc[predict[1][0][i],:])
    #if i !=0 : print(np.array(newFilm.title)[i]) # Affiche que le nom des films
newFilm #Debug
