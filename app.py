import pandas as pd
import numpy as np
import streamlit as st


df = pd.read_csv("./imdb_movie.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Movie Reco")  # add a title
#st.write(df)  # visualize my dataframe in the Streamlit app

#answ = st.multiselect('Votre film préféré', df.title)
ans = st.selectbox ('Votre film préféré',label (''),options (df.title))

def test(answ):
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

       predict = distanceKNN.kneighbors(X_scaled[imdb.title.str.lower() == ans]) 

       newFilm = pd.DataFrame(columns = imdb.columns) 
       for i in range(6):
              if stop == 1: break
              newFilm = newFilm.append(imdb.iloc[predict[1][0][i],:])
              #if i !=0 : print(np.array(newFilm.title)[i]) # Affiche que le nom des films
              return newFilm #Debug

#st.write(newFilm)
