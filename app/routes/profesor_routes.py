from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.db import get_db_connection

profesor_bp = Blueprint('profesor', __name__)

@profesor_bp.route('/profesores/<slug>')
def profesor_detalle(slug):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    page = int(request.args.get('page', 1))
    per_page = 3
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT p.ID_profesor, p.Nombre AS nombre_profesor, f.Nombre AS nombre_facultad
        FROM Profesores p
        LEFT JOIN Facultades f ON p.ID_facultad = f.ID_facultad
        WHERE p.Slug = %s
    """, (slug,))
    profesor = cur.fetchone()

    if not profesor:
        flash("Profesor no encontrado", "warning")
        return redirect(url_for('main.dashboard'))

    # Aquí extraemos el id del profesor para usarlo en las siguientes consultas
    id = profesor['ID_profesor']

    cur.execute("""
        SELECT m.Nombre AS nombre_materia
        FROM Materias m
        INNER JOIN profesores_materias pm ON m.ID_materia = pm.ID_materia
        WHERE pm.ID_profesor = %s
    """, (id,))
    materias = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total FROM Evaluaciones WHERE ID_profesor = %s", (id,))
    total_eval = cur.fetchone()['total']
    total_pages = (total_eval + per_page - 1) // per_page

    cur.execute("""
        SELECT ID_evaluacion, Estrellas, Comentario, Fecha, ID_usuario
        FROM Evaluaciones
        WHERE ID_profesor = %s
        ORDER BY Fecha DESC
        LIMIT %s OFFSET %s
    """, (id, per_page, offset))
    evaluaciones = cur.fetchall()

    promedio = None
    if total_eval > 0:
        cur.execute("SELECT AVG(Estrellas) AS promedio FROM Evaluaciones WHERE ID_profesor = %s", (id,))
        promedio = cur.fetchone()['promedio']
        if promedio is not None:
            promedio = round(promedio, 2)

    cur.close()
    conn.close()

    return render_template('profesor_detalle.html',
                           profesor=profesor,
                           materias=materias,
                           evaluaciones=evaluaciones,
                           promedio=promedio,
                           page=page,
                           total_pages=total_pages)

    
@profesor_bp.route('/profesores')
def listar_profesores():
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
    return render_template('profesores_lista.html', profesores=profesores)

