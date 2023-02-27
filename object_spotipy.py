from spotipy.oauth2 import SpotifyClientCredentials 
import multiprocessing as mp
import re

class aux_Spotipy:
    
    def __init__(self, id, secret, spotipy):
        self.client_id = id
        self.client_credentials_manager = secret
        self.sp = spotipy
    
    def playlist_URL_to_URI(self, link):
    # propos: convierte la URL de una playlist en un URI 
    # prec = la URl de una playlist de spotify
        uri = link.split("/")[-1].split("?")[0]
        return uri

    def clean_Title(self, title):
        # propos: limpiar el titulo para buscarlo en YTmusic
        # prec = string, el titulo de una cancion
        prepared_Title = re.sub(' +', ' ', title.replace('(','').replace(')','').replace('-','').replace('\'','').replace('\"','').strip())
        return prepared_Title

    def artist_Name(self, media):
        # propos: encontrar el nombre de un artista en el dict de la esta
        # prec = dict con la estructura correcta
        found_Artist = media["artists"][0]["name"].strip()
        return found_Artist

    def track_Name(self, track):
        # propos: encontrar el nombre de una cancion en el dict de esta
        # prec = dict con la estructura correcta
        track_Name = track["track"]["name"]
        return track_Name

    def get_Track(self, name):
        # propos: buscar un nombre en spotify
        # prec = string con el nombre y objeto spotipy
        result = self.sp.search(name)
        track = result["tracks"]["items"][0]
        return track

    def track_Album(self, track):
        # propos: encontrar el alvum asociado a una cancion
        # prec = dict de la cancion, y objeto spotipy
        album = self.sp.album(track["album"]["external_urls"]["spotify"])
        return album

    def track_Artist(self, track):
        # propos: encontrar el artista asociado a una cancion
        # prec = dict de la cancion, y objeto spotipy
        artist = self.sp.artist(track["artists"][0]["external_urls"]["spotify"])
        return artist

    def tracklist(self, playlist_URL, total_Length):
        # propos: devuelve todos los tracks de una playlist
        # prec = URL de la playlist, cantidad de nombres a devolver y un objeto Spotipy iniciado 
        tracklist = {}
        track_number = 0
        current_Offset = 0
        uri = self.playlist_URL_to_URI(playlist_URL)
        while(current_Offset < total_Length):
            for track in self.sp.playlist_tracks(uri, offset=current_Offset)["items"]:
                tracklist[track_number] = track
                track_number+=1
            current_Offset +=100
        return tracklist

    def get_Item_Data(self, item):
        try:
            track_Name = self.track_Name(item)
            print("paso track_Name")
            track = self.get_Track(track_Name, self.sp())
            print("paso track_Name")
            artist_Genres = (self.track_Artist(track, self.sp)["genres"])
            print("paso track_Name")
            album_Release_Date = (self.track_Album(track, self.sp())["release_date"])
            print("paso track_Name")
            data = (str(track_Name), artist_Genres, str(album_Release_Date))
            return(data)
        except:
            return("search error")


    def get_Playlist_Data(self, items):
        with mp.Pool(23) as p:
            async_result = p.map_async(self.get_Item_Data, items)
            results = async_result.get()
            return results

    