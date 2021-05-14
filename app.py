import os
from flask import Flask, make_response,jsonify, render_template, request
from dotenv import load_dotenv
from utils.controller import Movie
from flask_cors import CORS

load_dotenv(verbose=True)
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/fetchmovies', methods=['GET', 'POST'])
def fetch_movies():
    movie = Movie()
    limit = 10000
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    movies = movie.fetch_movies(limit)
    
    if not movies:
        return make_response('no movies available', 404)
    return make_response(jsonify(movies), 200)


@app.route('/api/v1/recommendations/<title>', methods=['GET', 'POST'])
def fetch_recommendations(title):
    movie = Movie()
    
    limit = 10000
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    
    movies = movie.fetch_recommendations(title, limit)
    
    if not movies:
        return make_response('', 200)
    return make_response(jsonify(movies), 200)


