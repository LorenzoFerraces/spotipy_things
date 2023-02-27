import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import auxiliares_spotipy as aux
import multiprocessing as mp
import time

#spotify app authentication
client_id = 'ID'
client_secret = "Secret" 

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) 

#spotify playlist url
mejunje = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"

#writing txt's
txt_genres = open('genres.txt', 'w')
txt_dates = open('dates.txt', 'w')

#getting a dict of all songs
lista = aux.tracklist (mejunje, 1200, sp)
valores = lista.values()

def get_Item_Data(item):
    try:
        track_Name = aux.track_Name(item)
        track = aux.get_Track(track_Name, sp)
        artist_Genres = (aux.track_Artist(track, sp)["genres"])
        album_Release_Date = (aux.track_Album(track, sp)["release_date"])
        data = (str(track_Name), artist_Genres, str(album_Release_Date))
        return(data)
    except:
        return("search error")


def get_Playlist_Data(items):
    with mp.Pool(23) as p:
        async_result = p.map_async(get_Item_Data, items)
        results = async_result.get()
        return results
    
    
if __name__ == '__main__':
    start_time = time.time()
    results = get_Playlist_Data(valores)
    for num, result in enumerate(results):
        try:
            txt_dates.write(result[0] + '; ' + result[2] + '\n')
            for genre in result[1]:
                txt_genres.write(result[0] + '; ' + str(genre) + '\n')
        except:
            print("write error with number " + str(num))
    print(time.time() - start_time, "seconds")
    
    