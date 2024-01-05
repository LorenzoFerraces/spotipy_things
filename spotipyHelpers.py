from collections.abc import Mapping, Iterable
import multiprocessing as mp
from functools import partial
import re



def playlist_URL_to_URI(link: str) -> str:
    # prop: convierte la URL de una playlist en un URI
    return link.split("/")[-1].split("?")[0]


def clean_title(title: str) -> str:
    # prop: limpiar el titulo para buscarlo en YTmusic
    return re.sub(
        " +",
        " ",
        title.replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace("'", "")
        .replace('"', "")
        .strip(),
    )


def track_name(track: str) -> str:
    # prop: encontrar el nombre de una cancion en el dict
    # prec = dict con la estructura correcta
    return track["track"]["name"].strip()


def search_track_album(spotipy: object, track: Mapping) -> str:
    # prop: encontrar el album asociado a una cancion
    # prec = dict de la cancion, y objeto spotipy
    return spotipy.album(track["album"]["external_urls"]["spotify"])


def search_track_artist(spotipy: object, track: Mapping) -> str:
    # propos: buscar el artista asociado a una cancion
    # prec = dict de la cancion, y objeto spotipy
    return spotipy.artist(track['track']["artists"][0]["external_urls"]["spotify"])


def release_date(track: Mapping) -> str:
    return track["track"]["album"]["release_date"].strip()


def artist_name(track: Mapping) -> str:
    return track["track"]["artists"][0]["name"].strip()


def tracklist(spotipy: object, playlist_URL: str, total_Length: int) -> Mapping:
    # propos: devuelve todos los tracks de una playlist
    # prec = URL de la playlist, cantidad de nombres a devolver y un objeto Spotipy iniciado
    tracklist = {}
    track_number = 0
    current_Offset = 0
    uri = playlist_URL_to_URI(playlist_URL)
    while current_Offset < total_Length:
        for track in spotipy.playlist_tracks(uri, offset=current_Offset)["items"]:
            tracklist[track_number] = track
            track_number += 1
        current_Offset += 100
    return tracklist


def get_item_data(spotipy: object, track: Mapping) -> tuple:
    try:
        name = track_name(track)
    except:
        return "error while retrieving name"
    artist = artist_name(track)
    try:
        artist_genres = search_track_artist(spotipy, track)['genres']
    except:
        print("error at search_track_artist")
    date = release_date(track)
    data = (str(name), str(artist), artist_genres, str(date))
    return data



def get_playlist_data(spotipy: object, items: Iterable) -> list:
    get_track_data = partial(get_item_data, spotipy)
    with mp.Pool(23) as p:
        async_result = p.map_async(get_track_data, items)
        return async_result.get()
