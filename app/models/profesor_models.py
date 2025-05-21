from app.db import get_db_connection

def obtener_profesor_por_slug(slug):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.ID_profesor, p.Slug, p.Nombre AS nombre_profesor, f.Nombre AS nombre_facultad
        FROM Profesores p
        LEFT JOIN Facultades f ON p.ID_facultad = f.ID_facultad
        WHERE p.Slug = %s
    """, (slug,))
    profesor = cur.fetchone()
    cur.close()
    conn.close()
    return profesor

def obtener_materias_por_profesor(id_profesor):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.Nombre AS nombre_materia
        FROM Materias m
        INNER JOIN profesores_materias pm ON m.ID_materia = pm.ID_materia
        WHERE pm.ID_profesor = %s
    """, (id_profesor,))
    materias = cur.fetchall()
    cur.close()
    conn.close()
    return materias

def obtener_total_evaluaciones(id_profesor):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM Evaluaciones WHERE ID_profesor = %s", (id_profesor,))
    total = cur.fetchone()['total']
    cur.close()
    conn.close()
    return total

def obtener_evaluaciones_paginadas(id_profesor, limit, offset):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT ID_evaluacion, Estrellas, Comentario, Fecha, ID_usuario
        FROM Evaluaciones
        WHERE ID_profesor = %s
        ORDER BY Fecha DESC
        LIMIT %s OFFSET %s
    """, (id_profesor, limit, offset))
    evaluaciones = cur.fetchall()
    cur.close()
    conn.close()
    return evaluaciones

def obtener_promedio_estrellas(id_profesor):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT AVG(Estrellas) AS promedio FROM Evaluaciones WHERE ID_profesor = %s", (id_profesor,))
    promedio = cur.fetchone()['promedio']
    cur.close()
    conn.close()
    return round(promedio, 2) if promedio else None

def listar_profesores_con_promedio():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.ID_profesor, p.Nombre, p.Slug, p.Correo_institucional, f.Nombre AS Facultad,
            COALESCE(ROUND(AVG(e.Estrellas), 1), 0) AS Promedio
        FROM Profesores p
        LEFT JOIN Facultades f ON p.ID_facultad = f.ID_facultad
        LEFT JOIN Evaluaciones e ON p.ID_profesor = e.ID_profesor
        GROUP BY p.ID_profesor
        ORDER BY p.Nombre ASC
    """)
    profesores = cur.fetchall()
    cur.close()
    conn.close()
    return profesores
