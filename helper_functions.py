import psycopg
import configparser
from urllib.parse import urlparse

def load_config(filename='database_local.ini', isURL=False):

    # Check for DATABASE_URL environment variable
    # Load from database.ini if DATABASE_URL is not set
    parser = configparser.RawConfigParser()
    parser.read(filename)

    section = 'postgres'
    key_value_pair_postgres = parser.items(section)
    params_parsed = {i[0]: i[1] for i in key_value_pair_postgres}
    

    if not isURL:
        pg_connection_dict = {
            'dbname': params_parsed['dbname'],
            'user': params_parsed['user'],
            'password': params_parsed['password'],
            'port': params_parsed['port'],
            'host': params_parsed['host']
        }

    elif isURL:
        conStr = parser.items(section)[0][1]
        url_parsed = urlparse(conStr)

        pg_connection_dict = {
            'dbname': url_parsed.path[1:],
            'user': url_parsed.username,
            'password': url_parsed.password,
            'port': url_parsed.port,
            'host': url_parsed.hostname
        }

    return pg_connection_dict

def connect(config):
    try:
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            print(conn)
        return psycopg.connect(**config) 
    except (psycopg.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    try:
        conn = connect(load_config(filename='database_local.ini'))
        print(conn)
    except Exception as e:
        print(f'error {e}')
        conn.close()
    finally:
        print('conn closed')
        conn.close()