import mariadb, sys, os

def get_db_connection():
    try:
        conn = mariadb.connect(
            user='root',
            password='12345',
            host='localhost',
            port=3306,
            database='upconnect'
        )
        return conn
    except mariadb.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        sys.exit(1)
