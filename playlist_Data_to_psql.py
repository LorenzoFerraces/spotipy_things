import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import multiprocessing as mp
from configparser import ConfigParser
import psycopg2  

import auxiliares_spotipy as aux
from auxiliares_DB import config

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

#extracting the values from that dict
valores = lista.values()

#connect to database "musica"
params = config()
conn = psycopg2.connect(**params)

#create a cursor
cur = conn.cursor()

results =