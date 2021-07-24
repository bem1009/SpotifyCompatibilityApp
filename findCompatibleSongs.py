import requests
import re 
import json
import urllib

from requests.api import request

USER_IDS = ["https://api.spotify.com/v1/users/bmiller1550/playlists?limit=20", "https://api.spotify.com/v1/users/21o5gb3zdgw7grpnlha7sfu5y/playlists?limit=20",
            "https://api.spotify.com/v1/users/21o5gb3zdgw7grpnlha7sfu5y/playlists?limit=15&offset=20", "https://api.spotify.com/v1/users/tlounsy/playlists?limit=20"]

Profile = "https://api.spotify.com/v1/users/bmiller1550/playlists"
ACCESS_TOKEN = "BQDdnk8pJV8VANOaxapSBEStLumWK-1uGkx7qPnHdYcItzu89tBqhaoFCrd3QLajBnFhqKfdwm-BKMzHawfSQOJ-BmV2Ojly2CYZfF1mdDz9lW4-BvKKeMr4mgiDWtqT5hYrb65CJR92H1jo9AXpPdW--48_T80Utj5TJpNPEu7-Ljn3AN3_YKtUiOKMbDJyC1zEp_EzXXKoARecUck2CSDSbcY"


#FIXES - For some reason the "New Music Friday" Does not work. Every other playlist I've tried works 

def create_playlist_on_spotify(name, public):
    response = requests.post(
        Profile,
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

    query = urllib.parse.quote(f"{artist} {song}")
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"

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


def main(USER_PROFILES):
    songfreq = [{},{},{},{}]
    

    for i in range(len(USER_PROFILES)):
        playlists = get_user_playlists(USER_PROFILES[i])

        
    
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

    #find all the URIs for all the cross-referenced songs you found 
    if len(crossedSongs) != 0:
        uris = []
        playlist_identifier = create_playlist_on_spotify("New Playlist!",False)
        for i in range(len(crossedSongs)):
            uris = get_spotify_uri(crossedSongs[i][0], crossedSongs[i][1]) 
            add_song_to_playlist(playlist_identifier,uris)
        
    
    #print(playlist_identifier)
    

if __name__ == '__main__':
    main()