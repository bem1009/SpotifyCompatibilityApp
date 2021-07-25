from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import findCompatibleSongs
from secrets import *
import spotipy
from spotipy import oauth2
import time

#get the secretClientID from a local path
import keys
clientSecret = keys.main()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SESSION_COOKIE_NAME'] = 'CUR_COOKIE'
app.secret_key = "VsYB4ogop2"
db = SQLAlchemy(app)

spot_redirect_uri = "http://127.0.0.1:5000/"


AUTHORIZE = "https://accounts.spotify.com/authorize"
REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
clientID = "54b18b9335cf4489bbd682de84967d7f"

TOKEN_INFO="token_info"

CUR_TOKEN = ""

@app.route("/", methods=["GET"])
def index():

    try:
        token_info = getToken()
    except:
        print("User not logged in")

    sp = spotipy.Spotify(auth=token_info['access_token'])

    return render_template("index.html")


def getToken():
    token_info = session.get(TOKEN_INFO,None)
    if token_info == None:
        raise "exception"
    now = int(time.time())
    
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


    

def callAuthorizationApi(url,code,path, client):
    response = requests.post(
        url,
        headers={
            "Authorization":client
        },
        json={
            "grant_type":"authorization_code",
            "code": code,
            "redirect_uri":path
        }
    )
    json_resp = response.json()
    print(json_resp)


@app.route("/loading", methods=["POST","GET"])
def loadingScreen():
    return render_template('processingPlaylists.html', form_data=request.form)

@app.route("/reqAccess")
def requestAccess():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    print(url_for('index'))
    return redirect(url_for('index', _external=True))   

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



def create_spotify_oauth():
    return oauth2.SpotifyOAuth(
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri="http://127.0.0.1:5000/authorize",
        scope="playlist-modify-public playlist-modify-private"
    )



