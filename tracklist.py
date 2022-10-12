import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from ytmusicapi import YTMusic


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


for i in range(0,10):
    artist = tracklist[i].split(",")[-1].strip()
    title = tracklist[i].split(",")[0].strip()
    songs = ytmusic.search(tracklist[i], filter='songs')
    for result in songs:
        # print(result["artists"][0]["name"])
        result_Artist = result["artists"][0]["name"].strip()
        result_Title = result["title"].strip()
        print(result_Title, title)
        if result_Artist == artist and title == result_Title:
            print((result_Artist, artist), (result_Title, title))
        #     ytmusic.add_playlist_items(playlistId, [result['videoId']])
        # else:
        #     continue
        # break


