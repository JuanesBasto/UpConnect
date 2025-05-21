from app.db import get_db_connection
from datetime import datetime

def ya_evaluo(id_profesor, id_usuario):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Evaluaciones WHERE ID_profesor = %s AND ID_usuario = %s", (id_profesor, id_usuario))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def insertar_evaluacion(id_profesor, id_usuario, estrellas, comentario):
    fecha = datetime.now()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Evaluaciones (ID_profesor, ID_usuario, Estrellas, Comentario, Fecha)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_profesor, id_usuario, estrellas, comentario, fecha))
    conn.commit()
    cur.close()
    conn.close()

def actualizar_evaluacion(id_evaluacion, id_usuario, estrellas, comentario):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Evaluaciones
        SET Estrellas = %s, Comentario = %s, Fecha = CURDATE()
        WHERE ID_evaluacion = %s AND ID_usuario = %s
    """, (estrellas, comentario, id_evaluacion, id_usuario))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_evaluacion(id_profesor, id_usuario):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Evaluaciones
        WHERE ID_profesor = %s AND ID_usuario = %s
    """, (id_profesor, id_usuario))
    conn.commit()
    cur.close()
    conn.close()
