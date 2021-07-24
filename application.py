from re import template
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import findCompatibleSongs
import subprocess

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loading", methods=["POST","GET"])
def loadingScreen():
    return render_template('processingPlaylists.html', form_data=request.form)

    

@app.route('/process', methods=["POST","GET"])
def processing():
    if request.method == "POST":
        playlist_url = request.form
        profiles = []
        for value in playlist_url.values():
            value = "https://api.spotify.com/v1/users/" + value + "/playlists?limit=20"
            profiles.append(value)

        matchedSongs = findCompatibleSongs.main(profiles)

        print(matchedSongs)

    return render_template('results.html')