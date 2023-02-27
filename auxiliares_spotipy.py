import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import re

def playlist_URL_to_URI(link):
    # propos: convierte la URL de una playlist en un URI 
    # prec = la URl de una playlist de spotify
    uri = link.split("/")[-1].split("?")[0]
    return uri

def clean_Title(title):
    # propos: limpiar el titulo para buscarlo en YTmusic
    # prec = string, el titulo de una cancion
    prepared_Title = re.sub(' +', ' ', title.replace('(','').replace(')','').replace('-','').replace('\'','').replace('\"','').strip())
    return prepared_Title

def artist_Name(media):
    # propos: encontrar el nombre de un artista en el dict de la esta
    # prec = dict con la estructura correcta
    found_Artist = media["artists"][0]["name"].strip()
    return found_Artist

def track_Name(track):
    # propos: encontrar el nombre de una cancion en el dict de esta
    # prec = dict con la estructura correcta
    track_Name = track["track"]["name"]
    return track_Name

def get_Track(name, sp):
    # propos: buscar un nombre en spotify
    # prec = string con el nombre y objeto spotipy
    result = sp.search(name)
    track = result["tracks"]["items"][0]
    return track

def track_Album(track, sp):
    # propos: encontrar el alvum asociado a una cancion
    # prec = dict de la cancion, y objeto spotipy
    album = sp.album(track["album"]["external_urls"]["spotify"])
    return album

def track_Artist(track, sp):
    # propos: encontrar el artista asociado a una cancion
    # prec = dict de la cancion, y objeto spotipy
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    return artist

def tracklist(playlist_URL, total_Length, sp):
    # propos: devuelve todos los tracks de una playlist
    # prec = URL de la playlist, cantidad de nombres a devolver y un objeto Spotipy iniciado 
    tracklist = {}
    track_number = 0
    current_Offset = 0
    uri = playlist_URL_to_URI(playlist_URL)
    while(current_Offset < total_Length):
        for track in sp.playlist_tracks(uri, offset=current_Offset)["items"]:
            tracklist[track_number] = track
            track_number+=1
        current_Offset +=100
    return tracklist
    
def get_Playlist_Names(tracklist):
    # propos: devuelve el nombre de todos los elementos de una playlist
    # prec = URL de la playlist, cantidad de nombres a devolver y un objeto Spotipy iniciado 
    for key, value in tracklist.items():
        print(key, '->', value)
        
def get_playlist_data(values, sp):
    try:
        track_Name = track_Name(values)
        track = get_Track(track_Name, sp)
        artist_Genres = (track_Artist(track, sp)["genres"])
        album_Release_Date = (track_Album(track, sp)["release_date"])
        data = (str(track_Name), artist_Genres, str(album_Release_Date))
    except:
        data=("1: search error")
    return data
        