import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from ytmusicapi import YTMusic
import re


client_id = 'ID'
client_secret = "Secret" 

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) 

mejunje = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"

un = open('unavailable.txt', 'w')

#Funciones auxiliares

def clean_Title(title):
    prepared_Title = re.sub(' +', ' ', title.replace('(','').replace(')','').replace('-','').replace('\'','').replace('\"','').strip())
    return prepared_Title

def find_Artist(media):
    found_Artist = media["artists"][0]["name"].strip()
    return found_Artist

def get_Playlist_Items(playlist_Link, playlist_Length):
    tracklist = []
    track_number = 0
    current_Offset = 0
    uri = playlist_Link.split("/")[-1].split("?")[0]
    while(current_Offset < playlist_Length):
        for track in sp.playlist_tracks(uri, offset=current_Offset)["items"]:
            try:
                track_name = track["track"]["name"] + ", " + track["track"]["album"]["artists"][0]["name"]
                tracklist.append(track_name + " ")
            except:
                pass

            track_number+=1
        current_Offset +=100

    return tracklist





ytmusic = YTMusic('headers_auth.json')

playlistId = 'PLSjB2BQNsuuWvk73iIFwtGO1xiwl_BNj3'



for track in get_Playlist_Items(mejunje, 1200):

    artist = track.split(",")[-1].strip().split(' ')[0].lower()

    title = re.sub(' +', ' ', track.split(",")[0].replace('(','').replace(')','').replace('-','')).lower()

    songs = ytmusic.search(track, filter='songs')
    videos = ytmusic.search(track, filter='videos')

    for song, video in zip(songs, videos):

        song_Artist  = find_Artist(song).lower()
        video_Artist = find_Artist(video).lower()
        song_Title  = clean_Title(song['title']).lower()
        video_Title = clean_Title(video['title']).lower()

        if artist in song_Artist and title in song_Title:
            print(title + " added succesfully" + " as song")
            ytmusic.add_playlist_items(playlistId, [song['videoId']])
            pass
        elif title in video_Title and artist in video_Artist:
            print(video_Title + " added succesfully" + " as video")
            ytmusic.add_playlist_items(playlistId, [video['videoId']])
        else:
            # print(title + " wasn't available:")
            try:
                un.write(title + ' by ' + artist + " wasn't found, " + video_Title + ", by " + video_Artist + " was found instead" + '\n')
            except:
                pass
            break
        break

