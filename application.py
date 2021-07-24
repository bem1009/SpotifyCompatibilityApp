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

@app.route("/callScript", methods=['POST'])
def processPlaylists():

    findCompatibleSongs.main()


@app.route('/process', methods=["POST"])
def processing():
    playlist_url = request.form
    return playlist_url
    
    
    #return render_template('processingPlaylists.html')