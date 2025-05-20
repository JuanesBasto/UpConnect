import mariadb

try:
    conn = mariadb.connect(
        user="root",
        password="12345",  # pon aquí tu contraseña de root de MariaDB
        host="localhost",
        port=3306,
        database="UpConnect"
    )
    print("Conexión exitosa a la base de datos!")
    conn.close()

except mariadb.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
