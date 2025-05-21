from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.db import get_db_connection

profesor_bp = Blueprint('profesor', __name__)

@profesor_bp.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return render_template("dashboard.html")
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("auth.login"))

@profesor_bp.route('/profesores/<int:id>')
def profesor_detalle(id):
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
        WHERE p.ID_profesor = %s
    """, (id,))
    profesor = cur.fetchone()

    if not profesor:
        flash("Profesor no encontrado", "warning")
        return redirect(url_for('profesor.dashboard'))

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
