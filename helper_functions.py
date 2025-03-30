import psycopg2
import configparser
from urllib.parse import urlparse

def load_config(filename='database_remote.ini', section='postgres'):
    db_config = {}

    # Check for DATABASE_URL environment variable
    # Load from database.ini if DATABASE_URL is not set
    parser = configparser.RawConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    # Parse the DATABASE_URL from the ini file if present
    if 'database_url' in db_config:
        url = urlparse(db_config['database_url'])
        db_config = {
            'host': url.hostname,
            'database': url.path[1:],  # Remove leading '/'
            'user': url.username,
            'password': url.password,
            'port': url.port
        }
        

    return db_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    print(connect(load_config(filename='database_local.ini')))