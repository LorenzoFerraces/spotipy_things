import psycopg2  
import auxiliares_DB as aux_DB


#spotify playlist url
mejunje = "https://open.spotify.com/playlist/6DaFmf4BQVBRAonTp749vW?si=2b2c3e7b19af4357"

#opening txt's
txt_genres = open('genres.txt',"r" )
txt_dates = open('dates.txt', "r")

#connect to database "musica"
params = aux_DB.config()
conn = psycopg2.connect(**params)

#create a cursor
cur = conn.cursor()

def clear_Single_Quote(string):
    list = string.split('\'')
    result = ''.join(list)
    return result
        

def insert_Into_Release(dates):
    for line in dates:
        try:
            raw_Name = line.split(';')[0].strip()
            name = "\'" + clear_Single_Quote(raw_Name) + "\'"
            raw_Artist = line.split(';')[1].strip()
            artist = "\'" + clear_Single_Quote(raw_Artist) + "\'"
            raw_Date = line.split(';')[2].strip()
            yyyy_mm_dd = raw_Date.split('-') 
            if(len(yyyy_mm_dd) < 3):
                continue
            date = "\'" + clear_Single_Quote(raw_Date) + "\'"
        except:
            print("problem with ")
        query = aux_DB.insert_release(name, artist, date)

        cur.execute(query)
        db_dump = cur.fetchone()
        print(db_dump)


        
def insert_Into_Genres(genres):
    for line in genres:
        raw_Name = line.split(';')[0].strip()
        name = "\'" + clear_Single_Quote(raw_Name) + "\'"
        raw_Artist = line.split(';')[1].strip()
        artist = "\'" + clear_Single_Quote(raw_Artist) + "\'"
        raw_genre = line.split(';')[2].strip()
        genre = "\'" + clear_Single_Quote(raw_genre) + "\'"
        query = aux_DB.insert_genres(name, artist, genre)
        cur.execute(query)
        db_dump = cur.fetchone()
        print(db_dump)




if __name__ == '__main__':

    insert_Into_Release(txt_dates)
    insert_Into_Genres(txt_genres)
    conn.commit()
    cur.close()


