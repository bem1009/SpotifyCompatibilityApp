import requests
import re 
import json
from secrets import spotify_user_id, spotify_token

from requests.api import request

USER_IDS = ["https://api.spotify.com/v1/users/bmiller1550/playlists?limit=20", "https://api.spotify.com/v1/users/21o5gb3zdgw7grpnlha7sfu5y/playlists?limit=20",
            "https://api.spotify.com/v1/users/21o5gb3zdgw7grpnlha7sfu5y/playlists?limit=15&offset=20", "https://api.spotify.com/v1/users/tlounsy/playlists?limit=20"]
ACCESS_TOKEN = "BQDL3-LyanZ274Gw7FTdlbEa-RVlFfiB3G-yoMwwf1gliALsQxPsgv_ng5tpphoJkjODoDWd0x2nbzVhTuemTZ2LkFtBbKTCMypoIAT1cEmnyAZY4VYgbSFnWRsgVYFfTOakXxnizcanYqo10AuJYUrZyawXvUQ"


#FIXES - For some reason the "New Music Friday" Does not work. Every other playlist works however

def create_playlist_on_spotify(name, public):
    response = requests.post(
        USER_ID,
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
    return json_resp


def get_user_playlists(USER_ID):
    response = requests.get(
        USER_ID,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        
    )
    json_resp = response.json()
    return json_resp


def get_playlist_songs(playlist_urls,songcount):
    
    # need to make (songcount // 30) api calls to get all songs in playlist
    #if songcount > 50:
        #songcount = 50
    iterations = (songcount // 30) + 1 
    remainder = songcount % 30
    offset = 0
    songs = []
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
        #print(len(items))
        
        for item in items:
            #print(item)
            #print(item["track"]["artists"][0]["name"])
            songs.append( (item["track"]["artists"][0]["name"], item["track"]["name"]) )
            #print(item["track"]["name"])
            
        
        offset += 30
        
        playlist_urls = re.sub(r'offset=\d+', 'offset=' + str(offset), playlist_urls)
   

    return songs

def create_playlist(songs):
    request_body = json.dumps({
        "name": "PlayList!",
        "description": "All Compatible Spotify Songs",
        "public" : True 

    })

    query = "https://api.spotify.com/v1/users/bmiller1550/playlists"

    response = requests.post(
        query,
        data = request_body,
        headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer {}".format(spotify_token)

        }
    )
    response_json = response.json()

    #return playlist ID
    return response_json["id"]


def main():
    songfreq = [{},{},{},{}]
    

    for i in range(len(USER_IDS)):
        playlists = get_user_playlists(USER_IDS[i])

        
    
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
    
    
    
        #print(songcount)
        
        #print(playlist_urls[0])


        songs = []

        for j in range(len(playlist_urls)):
            #print(playlist_urls[2])
            #print(name[j])
            songs += get_playlist_songs(playlist_urls[j],songcount[j])
            
                

        #print(songs)
        for j in range(len(songs)):
            if songs[j] not in songfreq[i]:
                #print(songs[j])
                songfreq[i][songs[j]] = 1
            
        
        
        
        print(len(songs))
    
    
    crossedSongs = []
    for key in songfreq[0]:
        if key in songfreq[1] or key in songfreq[2] or key in songfreq[3]:
            crossedSongs.append(key)


    for song in crossedSongs:
        
        print(song)

    print(len(crossedSongs))
    

if __name__ == '__main__':
    main()