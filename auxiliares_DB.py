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


def insert_release(name_Param, release_date_Param):
    query =   """INSERT INTO release (name, release_date) VALUES ({name}, {release_date}) RETURNING name;""".format(name = name_Param, release_date = release_date_Param)
    return query