# =============================================
# File Name: application.py
# Author: Benjamin Miller
# 
# This file is used to build the web application 
# for the spotify compatibility app. 
# All appropriate routing can be found in here.
#
# =============================================
from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import findCompatibleSongs
from secrets import *
import spotipy
from spotipy import oauth2
import time
import re

#get the secretClientID from a local path
import keys
clientSecret = keys.main()[0]

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
application.config['SESSION_COOKIE_NAME'] = 'CUR_COOKIE'
application.secret_key = keys.main()[1]
db = SQLAlchemy(application)


AUTHORIZE = "https://accounts.spotify.com/authorize"
REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
clientID = "54b18b9335cf4489bbd682de84967d7f"

TOKEN_INFO="token_info"

CUR_TOKEN = ""

@application.route("/", methods=["GET"])
def index():
    '''
    Main page for Spotify Compatibility App.

    :return: render template for main page
    '''
    
    try:
        token_info = getToken()
    except:
        print("User not logged in")
        return redirect(url_for('authorize', _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])

    return render_template("index.html")


def getToken():
    '''
    Gets a token from the spotify API, if the token has expired, gets
    a refresh token.

    :return: the token info
    '''    
    token_info = session.get(TOKEN_INFO,None)
    if token_info == None:
        raise "exception"
    now = int(time.time())
    
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

@application.route("/reqAccess")
def requestAccess():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@application.route('/authorize')
def authorize():
    '''
    Retrieves the spotify API access token.

    :return: redirect to main page
    '''    
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('index', _external=True))   

@application.route("/errorHandler")
def errorHandler():
    '''
    This gets called called when the user does not put in a playlist name

    :return: returns erroroutput page
    '''    
    return render_template('erroroutput.html')


@application.route('/process', methods=["POST","GET"])
def processing():
    '''
    This is called when the user hits the "SUBMIT" button on the main page.
    It kicks off findCompatibleSongs.py and presents a loading screen while doing
    so. It returns a results page when finished

    :return: the results page
    '''    
    if request.method == "POST":
        playlist_url = request.form
        profiles = []
        playlist_name = ""
        #handle redirect for bad inputs

        if playlist_url["PlaylistName"] == "":
            return redirect(url_for("errorHandler",_external=True))


        for key,value in playlist_url.items():
            if key == "PlaylistName":
                playlist_name = value
            else:
                value = "https://api.spotify.com/v1/users/" + value + "/playlists?limit=20"
                profiles.append(value)

        successOrFail = findCompatibleSongs.main(profiles,playlist_name)
        if successOrFail != "SUCCESS" or successOrFail != "":
            #remove the prefix and suffix from the string to just get profile name
            prefix = "https://api.spotify.com/v1/users/"
            suffix = "/playlists?limit=20"
            if successOrFail.startswith(prefix):
                successOrFail = successOrFail[len(prefix):]
            
            if successOrFail.endswith(suffix):
                successOrFail = successOrFail[:-len(suffix)]

            
            
            return render_template("wrongProfile.html", errorProfile = successOrFail)

    return render_template('results.html')


@application.route("/wrongProfile")
def wrongProfile(errorProfile):
    '''
    Called when user inputs a profile that cannot be found within the spotify API

    :return: wrongProfile page
    '''    
    return render_template('wrongProfile.html')



def create_spotify_oauth():
    '''
    Creates an outh2 instance from the spotifyOAuth library which
    is used to obtain/refresh tokens

    :return: returns an oauth2 instance
    '''    
    return oauth2.SpotifyOAuth(
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri="http://127.0.0.1:5000/authorize",
        scope="playlist-modify-public playlist-modify-private"
    )

if __name__ == "__main__":
    application.run()



