import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from object_spotipy import aux_Spotipy as objsp
import time

#spotify app authentication
client_id = 'ID'
client_secret = "Secret" 

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) 

#aux object init
aux = objsp('ID', "Secret", sp)

#spotify playlist url
mejunje = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"


#writing txt's
txt_genres = open('genres.txt', 'w')
txt_dates = open('dates.txt', 'w')

#getting a dict of all songs
lista = aux.tracklist(mejunje, 1400)
valores = lista.values()
    


if __name__ == '__main__':
    start_time = time.time()
    results = aux.get_Playlist_Data(valores)
    for num, result in enumerate(results):
        try:
            #descartar resultados erroneos
            if result[0] == 's':
                continue
            #quitar ";" de nombre de canciones
            song_name = result[0].replace(';',' ')
            txt_dates.write(song_name + '; ' + result[1] + '; ' +  result[3] + '\n')
            for genre in result[2]:
                txt_genres.write(song_name + '; ' + str(genre) + '\n')
        except:
            print("write error with number " + str(num))
    print(time.time() - start_time, "seconds")
    
