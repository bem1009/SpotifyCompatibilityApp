# =============================================
# File Name: findCompatibleSongs.py
# Author: Benjamin Miller
# 
# Used to interact with the spotify API and retrieve
# user playlist information, it then returns the songs
# that are compatible between multiple users
# =============================================

from logging import error
import requests
import re 
import json
import urllib
import application

from requests.api import request

def create_playlist_on_spotify(name, public,USER_PROFILE):
    '''
    Create a playlist on associated spotify account.

    :param p1: The name of the playlist 
    :param p2: the User profile to create the playlist on.

    :return: returns the JSON response to the request
    '''
    token_info = application.getToken()
    ACCESS_TOKEN = token_info['access_token']
    response = requests.post(
        USER_PROFILE,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}" 
        },
        json={
            #name is required
            "name":name,
            #the rest is optional
            "public":public
        }
    )
    json_resp = response.json()
    return json_resp["id"]


def get_spotify_uri(artist,song):
    '''
    Get the spotify uri associated with a song.

    :param p1: The artist of the song
    :param p2: the name of the song

    :return: returns the spotify uri associated with the song.
    '''    

    query = urllib.parse.quote(f"{artist} {song}")
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"

    token_info = application.getToken()
    ACCESS_TOKEN = token_info['access_token']

    response = requests.get(
        url,
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

    )
    response_json = response.json()
    results = response_json["tracks"]["items"]

    if results:
        return results[0]["id"]
    
    else:
        return None 


def add_song_to_playlist(playlist_id, song_uri):
    '''
    Add songs to a spotify playlist

    :param p1: the playlist ID value used for interacting with API
    :param p2: the specific song URI to find the song.

    :return: returns True if the Spotify API was less than 400 (non error), False otherwise
    '''
    token_info = application.getToken()
    ACCESS_TOKEN = token_info['access_token']
    query = urllib.parse.quote(f"spotify:track:{song_uri}")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={query}"

    response = requests.post(
        url,
        json = {
            "ids": song_uri
        },
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )
    response.json = response.json()
    
    return response.ok



def get_user_playlists(USER_ID):
    '''
    Get the first 20 user playlists

    :param p1: The username of the spotify account that we will get playlists from

    :return: returns the JSON response to the request
    '''
    token_info = application.getToken()
    ACCESS_TOKEN = token_info['access_token']
    response = requests.get(
        USER_ID,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        
    )
    if response.status_code == 404:
        return {}
    json_resp = response.json()
    return json_resp


def get_playlist_songs(playlist_urls,songcount):
    '''
    Get every song in a given playlist

    :param p1: the uri to the playlist
    :param p2: the amount of songs in said playlist

    :return: returns a list of all the songs in the playlist
    '''
    iterations = (songcount // 30) + 1 
    remainder = songcount % 30
    offset = 0
    songs = []
    token_info = application.getToken()
    ACCESS_TOKEN = token_info['access_token']
    for i in range(iterations):
        response = requests.get(
            playlist_urls,
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        )
        if response == 429:
            print("rate limit broken")
            break
        json_resp = response.json()
        items = json_resp["items"]
        
        
        for item in items:
            songs.append( (item["track"]["artists"][0]["name"], item["track"]["name"]) )
            
        offset += 30
        
        playlist_urls = re.sub(r'offset=\d+', 'offset=' + str(offset), playlist_urls)
   

    return songs

songfreq = [{},{},{},{}]
def retrieveUserSongs(USER_PROFILE,num):
    '''
    Get all the songs for every playlist a user might have

    :param p1: The user profile name 
    :param p2: The specific profile index in the form 

    :return: returns a -1 if couldn't find the user id, 0 otherwise
    '''
    playlists = get_user_playlists(USER_PROFILE)
    if playlists == {}:
        return -1

    items = playlists["items"]
    playlist_urls = []
    songcount = []
    name = []
    
    for j in range(len(items)):
        
        totalsongs = items[j]["tracks"]["total"]

        url = items[j]["href"]
        url += '/tracks?limit=30&offset=0'
        
        playlist_urls.append(url)
        name.append(items[j]["name"])
        songcount.append(items[j]["tracks"]["total"])

    songs = []

    for j in range(len(playlist_urls)):
        songs += get_playlist_songs(playlist_urls[j],songcount[j])
            
                
    for j in range(len(songs)):
        if songs[j] not in songfreq[num]:
            songfreq[num][songs[j]] = 1
            
    print(len(songs))
    return 0

def retrieveAllSongs(USER_PROFILES):
    '''
    Get every song for every profile

    :param p1: the list of profiles put into the form.

    :return: return "SUCCESS" is successful, and the invalid 
    USER profile if not successful.
    '''

    for i in range(len(USER_PROFILES)):
        errorcode = retrieveUserSongs(USER_PROFILES[i],i)
        if errorcode == -1:
            return USER_PROFILES[i]
    return "SUCCESS"


def main(USER_PROFILES, playlist_name):
    '''
    Finds every user's top playlists and songs, and creates a playlist
    with the most compatible songs between all users.

    :param p1: the list of profiles put into the form.
    :param p2: the name of the playlist to be created.

    :return: return "SUCCESS" is successful, and the invalid 
    USER profile if not successful.
    '''    
    
    errorMessage = retrieveAllSongs(USER_PROFILES)
    if errorMessage != "SUCCESS":
        return errorMessage 
    crossedSongs = []
    for key in songfreq[0]:
        if key in songfreq[1] or key in songfreq[2] or key in songfreq[3]:
            crossedSongs.append(key)


    #find all the URIs for all the cross-referenced songs you found 
    if len(crossedSongs) != 0:
        uris = []
        playlist_identifier = create_playlist_on_spotify(playlist_name,False,USER_PROFILES[0])
        for i in range(len(crossedSongs)):
            uris = get_spotify_uri(crossedSongs[i][0], crossedSongs[i][1]) 
            add_song_to_playlist(playlist_identifier,uris)

    return "SUCCESS"
        
if __name__ == '__main__':
    main()