import mariadb

def get_db_connection():
    conn = mariadb.connect(
        user='root',
        password='12345',
        host='localhost',
        port=3306,
        database='upconnect'
    )
    return conn
