from flask import Flask, request
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1> Welcome to the moviest api </h1>'


if __name__ == '__main__':
    app.run(debug=True)