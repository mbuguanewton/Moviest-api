import os
from flask import Flask, make_response,jsonify, render_template
from dotenv import load_dotenv
from .utils.controller import Movie
from flask_cors import CORS

load_dotenv(verbose=True)
app = Flask(__name__)
CORS(app, resources={r"/api/*":{"origin":"*"}} )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/fetchmovies', methods=['GET', 'POST'])
def fetch_movies():
    movie = Movie()
    movies = movie.fetch_movies()
    
    if not movies:
        return make_response('no movies available', 404)
    return make_response(jsonify(movies), 200)


@app.route('/api/v1/recommendations/<title>', methods=['GET', 'POST'])
def fetch_recommendations(title):
    movie = Movie()
    movies = movie.fetch_recommendations(title)
    
    if not movies:
        return make_response('no recommendations available', 200)
    return make_response(jsonify(movies), 200)


