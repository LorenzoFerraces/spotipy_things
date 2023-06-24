from configparser import ConfigParser
import psycopg2  

class db_user():

    def __init__(self, filename, section):
        params = self.__config(filename, section)
        self.__connection = psycopg2.connect(**params)
        self.__cur = self.__connection.cursor()

    def __config(self, filename, section):
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

    def clear_single_quote(self, string):
        list = string.split('\'')
        result = ''.join(list)
        return result

    def insert_release(self, name_Param, artist_Param, release_date_Param):
        query =   """INSERT INTO release (name, artist, release_date) VALUES ({name}, {artist}, {release_date}) RETURNING name, artist;""".format(
            name = name_Param, artist = artist_Param, release_date = release_date_Param)
        return query

    def insert_genres(self, name_Param, artist_Param, genre_Param):
        query =   """INSERT INTO genres (name, artist, genre) VALUES ({name}, {artist}, {genre}) RETURNING name, genre;""".format(
            name = name_Param, artist = artist_Param, genre = genre_Param)
        return query

    def export_into_release(self, dates):
        for line in dates:
            try:
                raw_Name = line.split(';')[0].strip()
                name = "\'" + self.clear_single_quote(raw_Name) + "\'"
                raw_Artist = line.split(';')[1].strip()
                artist = "\'" + self.clear_single_quote(raw_Artist) + "\'"
                raw_Date = line.split(';')[2].strip()
                yyyy_mm_dd = raw_Date.split('-') 
                if(len(yyyy_mm_dd) < 3):
                    continue
                date = "\'" + self.clear_single_quote(raw_Date) + "\'"
            except:
                print("problem with ")
            query = self.insert_release(name, artist, date)

            self.__cur.execute(query)
            db_dump = self.__cur.fetchone()
            print(db_dump)
        self.__connection.commit()



    def export_into_genres(self, genres):
        for line in genres:
            raw_Name = line.split(';')[0].strip()
            name = "\'" + self.clear_single_quote(raw_Name) + "\'"
            raw_Artist = line.split(';')[1].strip()
            artist = "\'" + self.clear_single_quote(raw_Artist) + "\'"
            raw_genre = line.split(';')[2].strip()
            genre = "\'" + self.clear_single_quote(raw_genre) + "\'"
            query = self.insert_genres(name, artist, genre)
            self.__cur.execute(query)
            db_dump = self.__cur.fetchone()
            print(db_dump)
        self.__connection.commit()


    def clean_Table(self, table_Name):
        query = """DELETE from {name};""".format(name=table_Name)
        self.__cur.execute(query)
    
    def close_cursor(self):
        self.__cur.close()