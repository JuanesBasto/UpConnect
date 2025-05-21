from app.db import get_db_connection
from werkzeug.security import generate_password_hash

def obtener_carreras_por_facultad():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.ID_carrera, c.Nombre AS nombre_carrera, f.Nombre AS nombre_facultad
        FROM Carreras c
        JOIN Facultades f ON c.ID_facultad = f.ID_facultad
        ORDER BY f.Nombre, c.Nombre
    """)
    carreras_raw = cur.fetchall()
    cur.close()
    conn.close()

    from collections import defaultdict
    carreras_por_facultad = defaultdict(list)
    for carrera in carreras_raw:
        carreras_por_facultad[carrera["nombre_facultad"]].append({
            "ID_carrera": carrera["ID_carrera"],
            "nombre_carrera": carrera["nombre_carrera"]
        })
    return carreras_por_facultad

def buscar_usuario_por_correo(correo):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Usuarios WHERE Correo_institucional = ?", (correo,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def registrar_usuario(nombre, apellido, correo, contrasena, semestre, semillero, id_carrera):
    contrasena_hash = generate_password_hash(contrasena)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Usuarios (Nombre, Apellido, Correo_institucional, Contrasena, Fecha_registro, Semestre, Semillero, ID_carrera)
        VALUES (?, ?, ?, ?, CURDATE(), ?, ?, ?)
    """, (nombre, apellido, correo, contrasena_hash, semestre, semillero, id_carrera))
    conn.commit()
    cur.close()
    conn.close()
