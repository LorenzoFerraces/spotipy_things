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
        

for num, line in enumerate(txt_dates):
    try:
        raw_Name = line.split(';')[0].strip()
        name = "\'" + clear_Single_Quote(raw_Name) + "\'"
        raw_Date = line.split(';')[1].strip()
        yyyy_mm_dd = raw_Date.split('-') 
        if(len(yyyy_mm_dd) < 3):
            continue
        date = "\'" + clear_Single_Quote(raw_Date) + "\'"
    except:
        print("problem with ")
    query = aux_DB.insert_release(name, date)
    
    cur.execute(query)
    db_dump = cur.fetchone()
    print(db_dump)
    
    # print("error with query number " + str(num))



# conn.commit()
# cur.close()


