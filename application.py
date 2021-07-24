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



def callScript():
    findCompatibleSongs.main()

@app.route('/process')
def processing():
    #return render_template('processingPlaylists.html', subprocess_output=callScript() )
    return render_template('processingPlaylists.html')