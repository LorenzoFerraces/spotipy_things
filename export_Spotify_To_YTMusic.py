import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from ytmusicapi import YTMusic
import re
import auxiliares_spotipy as aux

client_id = 'ID'
client_secret = "Secret" 

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) 

mejunje = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"

un = open('unavailable.txt', 'w')

ytmusic = YTMusic('headers_auth.json')

playlistId = 'PLSjB2BQNsuuWvk73iIFwtGO1xiwl_BNj3'

lista = aux.tracklist (mejunje, 1200, sp)


if __name__ == "__main__":
    for track in lista:

        artist = track.split(",")[-1].strip().split(' ')[0].lower()

        title = re.sub(' +', ' ', track.split(",")[0].replace('(','').replace(')','').replace('-','')).lower()

        songs = ytmusic.search(track, filter='songs')
        videos = ytmusic.search(track, filter='videos')

        for song, video in zip(songs, videos):

            song_Artist  = aux.find_Artist(song).lower()
            video_Artist = aux.find_Artist(video).lower()
            song_Title  = aux.clean_Title(song['title']).lower()
            video_Title = aux.clean_Title(video['title']).lower()

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
