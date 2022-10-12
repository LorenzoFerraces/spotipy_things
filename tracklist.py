import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from ytmusicapi import YTMusic
import re


client_id = 'ID'
client_secret = "Secret" 

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) 

playlist_link = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI,)["items"]] 

tracklist = []
offset = 0
track_number = 0

while(offset < 1200):
    for track in sp.playlist_tracks(playlist_URI, offset=offset)["items"]:
        # print(track)
        try:
            track_name = track["track"]["name"] + ", " + track["track"]["album"]["artists"][0]["name"]

            tracklist.append(track_name + " ")

        except:
            pass
    
        track_number+=1

    offset+=100

t = open('tracks.txt', 'w')
for num, track in enumerate(tracklist):
    try:
        t.write(str(num) + ": " + track + '\n')
    except:
        t.write("track invalido")
# print(tracklist)


ytmusic = YTMusic('headers_auth.json')

playlistId = 'PLSjB2BQNsuuVbHpb5mueaaf7FqcttAmG8'


for i in range(0,20):

    artist = tracklist[i].split(",")[-1].strip()

    title = re.sub(' +', ' ', tracklist[i].split(",")[0].replace('(','').replace(')','').replace('-',''))

    songs = ytmusic.search(tracklist[i], filter='songs')

    for result in songs:
        result_Artist = result["artists"][0]["name"].strip()
        result_Title = re.sub(' +', ' ', result["title"].replace('(','').replace(')','').replace('-','').strip())
        if artist == result_Artist and title == result_Title:
            print(title + " added succesfully")
        #     ytmusic.add_playlist_items(playlistId, [result['videoId']])
        else:
            print(title + " wasn't available")
            break
        break


