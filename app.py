import os
from flask import Flask, make_response,jsonify
from dotenv import load_dotenv
from controller import Movie

load_dotenv(verbose=True)
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1> Welcome to the moviest api </h1>'


@app.route('/fetchMovies', methods=['GET', 'POST'])
def fetch_movies():
    movie = Movie()
    movies = movie.fetch_movies()
    
    if not movies:
        return make_response('no movies available', 404)
    return make_response(jsonify(movies), 200)


@app.route('/recommendations/<title>', methods=['GET', 'POST'])
def fetch_recommendations(title):
    movie = Movie()
    movies = movie.fetch_recommendations(title)
    
    if not movies:
        return make_response('no recommendations available', 200)
    return make_response(jsonify(movies), 200)


