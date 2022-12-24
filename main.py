from flask import Flask, redirect, url_for, jsonify
import map as mp

app = Flask(__name__)
mp.generate_map()


@app.route("/")
def hello_world():
    return f"<p>Добро пожаловать! С наступающим!</p>"


@app.route("/map")
def get_map():
    return jsonify([mp.houses, mp.players.values()])


@app.route("/reg")
def reg():
    pass

@app.route("/place_gift<id>")
def place(id: str):
    pass

@app.route("/score")
def score():
    pass