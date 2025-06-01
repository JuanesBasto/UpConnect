from app.db import get_db_connection

def obtener_foros_por_materia(id_materia):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT f.ID_foro, g.Grupo AS nombre_grupo
        FROM foros f
        LEFT JOIN grupos g ON f.ID_grupo = g.ID_curso
        WHERE f.ID_materia = %s
    """, (id_materia,))
    foros = cur.fetchall()
    cur.close()
    conn.close()
    return foros


def obtener_publicaciones_por_foro(id_foro):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.ID_publicacion, u.Nombre AS autor, p.Titulo, p.Contenido, p.Fecha
        FROM publicaciones_foro p
        INNER JOIN usuarios u ON p.ID_usuario = u.ID_usuario
        WHERE p.ID_foro = %s
        ORDER BY p.Fecha DESC
    """, (id_foro,))
    publicaciones = cur.fetchall()
    cur.close()
    conn.close()
    return publicaciones


def obtener_foro_por_id(id_foro):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT f.ID_foro, m.Nombre AS nombre_materia, g.Grupo AS nombre_grupo
        FROM foros f
        INNER JOIN materias m ON f.ID_materia = m.ID_materia
        LEFT JOIN grupos g ON f.ID_grupo = g.ID_grupo
        WHERE f.ID_foro = %s
    """, (id_foro,))
    foro = cur.fetchone()
    cur.close()
    conn.close()
    return foro
