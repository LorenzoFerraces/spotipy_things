from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def insert_release(name_Param, artist_Param, release_date_Param):
    query =   """INSERT INTO release (name, artist, release_date) VALUES ({name}, {artist}, {release_date}) RETURNING name, artist;""".format(
        name = name_Param, artist = artist_Param, release_date = release_date_Param)
    return query

def insert_genres(name_Param, genre_Param):
    query =   """INSERT INTO genres (name, genre) VALUES ({name}, {genre}) RETURNING name, genre;""".format(
        name = name_Param, genre = genre_Param)
    return query