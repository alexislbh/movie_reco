from flask import Flask, request, render_template
import pandas as pd
import streamlit as st

st.title('Uber pickups in NYC')
  
app = Flask(__name__)

imdb = pd.read_csv('imdb_movie.zip')

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        languages = imdb['title']
          
        return render_template("index.html", languages=languages)
  
  
if __name__ == '__main__':
    app.run(debug=True)
