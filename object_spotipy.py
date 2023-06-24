from spotipy.oauth2 import SpotifyClientCredentials 
import multiprocessing as mp
import re

class aux_Spotipy:
    
    def __init__(self, id, secret, spotipy):
        self.__client_id = id
        self.__client_credentials_manager = secret
        self.__sp = spotipy
        
    @property
    def sp(self):
        return self.__sp
    
    def playlist_URL_to_URI(self, link):
    # propos: convierte la URL de una playlist en un URI 
    # prec = la URl de una playlist de spotify
        return link.split("/")[-1].split("?")[0]

    def clean_Title(self, title):
        # propos: limpiar el titulo para buscarlo en YTmusic
        # prec = string, el titulo de una cancion
        return re.sub(' +', ' ', title.replace('(','').replace(')','').replace('-','').replace('\'','').replace('\"','').strip())

    def artist_Name(self, media):
        # propos: encontrar el nombre de un artista en el dict de la esta
        # prec = dict con la estructura correcta
        return (media["artists"][0]["name"].strip())
    
    def track_Name(self, track):
        # propos: encontrar el nombre de una cancion en el dict de esta
        # prec = dict con la estructura correcta
        return (track["track"]["name"])

    def get_Track(self, query, target_artist):
        # propos: buscar un nombre en spotify
        # prec = string con el nombre y objeto spotipy
        results = (self.sp).search(query)["tracks"]["items"]
        track = results[0]
        for result in results:
            result_artist = self.artist_Name(result)
            #ESTO NO VA A FUNCIONAR
            if (target_artist in result_artist):
                track = result
        return track

    def track_Album(self, track):
        # propos: encontrar el album asociado a una cancion cuando no tenemos el dato dentro de esta
        # prec = dict de la cancion, y objeto spotipy
        return (self.sp).album(track["album"]["external_urls"]["spotify"])

    def track_Artist(self, track):
        # propos: encontrar el artista asociado a una cancion cuando no tenemos el dato dentro de esta
        # prec = dict de la cancion, y objeto spotipy
        return (self.sp).artist(track["artists"][0]["external_urls"]["spotify"])

    def tracklist(self, playlist_URL, total_Length):
        # propos: devuelve todos los tracks de una playlist
        # prec = URL de la playlist, cantidad de nombres a devolver y un objeto Spotipy iniciado 
        tracklist = {}
        track_number = 0
        current_Offset = 0
        uri = self.playlist_URL_to_URI(playlist_URL)
        while(current_Offset < total_Length):
            for track in (self.sp).playlist_tracks(uri, offset=current_Offset)["items"]:
                tracklist[track_number] = track
                track_number+=1
            current_Offset +=100
        return tracklist

    def get_Item_Data(self, item):
        try:
            track_Name = self.track_Name(item).strip()
            artist = item["track"]["artists"][0]["name"].strip()
            query = track_Name + ' ' + artist
            print(query)
            track = self.get_Track(query, artist)
            artist_Genres = (self.track_Artist(track)["genres"])
            album_Release_Date = (self.track_Album(track)["release_date"]).strip()
            data = (str(track_Name), str(artist),  artist_Genres, str(album_Release_Date))
            return(data)
        except:
            return("search error")


    def get_Playlist_Data(self, items):
        with mp.Pool(23) as p:
            async_result = p.map_async(self.get_Item_Data, items)
            return async_result.get()


    