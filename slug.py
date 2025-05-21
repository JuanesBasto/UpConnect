import unidecode
import re
from app.db import get_db_connection

def generar_slug(nombre):
    nombre = unidecode.unidecode(nombre.lower())
    nombre = re.sub(r'[^a-z0-9]+', '-', nombre)
    return f"{nombre.strip('-')}"

conn = get_db_connection()
cur = conn.cursor()

cur.execute("SELECT ID_profesor, Nombre FROM Profesores")
profesores = cur.fetchall()

for id_profesor, nombre in profesores:
    slug = generar_slug(nombre)
    print(f"Actualizando {nombre} con slug {slug}")
    cur.execute("UPDATE Profesores SET Slug = %s WHERE ID_profesor = %s", (slug, id_profesor))

conn.commit()
cur.close()
conn.close()

