import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipyHelpers as aux
import auxiliares_DB as aux_DB

# spotify app authentication

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# aux object init


if __name__ == "__main__":
    action = int(
        input(
            "select 1 for dump release dates and genres per son into txt files"
            + "\n"
            + "select 2 for exporting those dumps into a postgres database"
            + "\n"
            + ":"
        )
    )

    if action == 1:
        # url de la playlist
        playlist = input("URL de la playlist, dejar vacio para usar mi playlist: ")
        if not playlist:
            playlist = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"

        # cantidad de canciones a tomar
        cantidad = int(input("Cantidad de canciones a contar: "))

        try:
            lista = aux.tracklist(sp, playlist, cantidad)
            valores = lista.values()
        except:
            raise Exception(
                "no se pudo obtener la lista de {cant} canciones de la playlist {url}".format(
                    cant=cantidad, url=playlist
                )
            )
        results = aux.get_playlist_data(sp, valores)
        txt_genres = open("genres.txt", "w")
        txt_dates = open("dates.txt", "w")
        txt_dates.write("name; artist; date" + "\n")
        txt_genres.write("name; artist; genre" + "\n")

        for num, result in enumerate(results):
            try:
                # descartar resultados erroneos
                if not isinstance(result, tuple):
                    print(f"resultado erroneo: {result}")
                    continue
                # quitar ";" de nombre de canciones
                song_name = result[0].replace(";", " ")
                artist = result[1]
                genres = result[2]
                release_date = result[3]
                txt_dates.write(f"{song_name} ; {artist} ; {release_date} \n")
                for genre in genres:
                    txt_genres.write(f"{song_name} ; {artist} ; {str(genre)}\n")
            except:
                print("write error with number " + str(num))

    elif action == 2:
        txt_genres = open("genres.txt", "r")
        txt_dates = open("dates.txt", "r")
        db = aux_DB.db_user("database.ini", "postgresql")
        db.clean_Table("release")
        db.clean_Table("genres")
        db.export_into_release(txt_dates)
        db.export_into_genres(txt_genres)
        db.close_cursor()
