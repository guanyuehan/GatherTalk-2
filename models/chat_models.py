import helper_functions 
import psycopg2

def insert_post_to_db(content: str):
    """ Insert a new post into the post table """

    sql = """INSERT INTO posts (content, created_at) VALUES(%s, NOW()) RETURNING post_id;""" #%s is placeholder

    post_id = None
    config = helper_functions.load_config(filename='database_local.ini')

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (content,))

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    post_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return post_id


def query_posts():
    sql = """SELECT post_id, content, created_at FROM posts ORDER BY created_at;"""

    config = helper_functions.load_config(filename='database_local.ini')

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

                rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return rows
    
if __name__ == '__main__':
    print(query_posts())