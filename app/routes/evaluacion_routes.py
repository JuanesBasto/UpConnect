from flask import Blueprint, request, redirect, session, url_for, flash, render_template
from app.db import get_db_connection
from datetime import datetime

evaluacion_bp = Blueprint('evaluacion', __name__)

@evaluacion_bp.route('/evaluar/<int:id>', methods=['POST'])
def agregar_evaluacion(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    estrellas = int(request.form['estrellas'])
    comentario = request.form.get('comentario') or ''
    fecha = datetime.now()

    if not (1 <= estrellas <= 5):
        flash("La calificación debe estar entre 1 y 5", "danger")
        return redirect(url_for('profesor.profesor_detalle', id=id))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Evaluaciones WHERE ID_profesor = %s AND ID_usuario = %s", (id, user_id))
    if cur.fetchone():
        flash("Ya has evaluado a este profesor", "warning")
        return redirect(url_for('profesor.profesor_detalle', id=id))

    cur.execute("""
        INSERT INTO Evaluaciones (ID_profesor, ID_usuario, Estrellas, Comentario, Fecha)
        VALUES (%s, %s, %s, %s, %s)
    """, (id, user_id, estrellas, comentario, fecha))
    conn.commit()
    cur.close()
    conn.close()

    flash("¡Gracias por tu evaluación!", "success")
    return redirect(url_for('profesor.profesor_detalle', id=id))

@evaluacion_bp.route('/evaluaciones/editar_ajax/<int:id_evaluacion>', methods=['POST'])
def editar_evaluacion_ajax(id_evaluacion):
    if 'user_id' not in session:
        return {'success': False, 'message': 'No autenticado'}, 401

    data = request.get_json()
    estrellas = data.get('estrellas')
    comentario = data.get('comentario')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Evaluaciones
        SET Estrellas = %s, Comentario = %s, Fecha = CURDATE()
        WHERE ID_evaluacion = %s AND ID_usuario = %s
    """, (estrellas, comentario, id_evaluacion, session['user_id']))
    conn.commit()
    cur.close()
    conn.close()
    
    flash("¡Evaluacion actualizada!", "success")
    return {'success': True, 'message': 'Evaluación actualizada'}


@evaluacion_bp.route('/evaluaciones/eliminar/<int:id_profesor>', methods=["POST"])
def eliminar_evaluacion(id_profesor):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Evaluaciones
        WHERE ID_profesor = %s AND ID_usuario = %s
    """, (id_profesor, session['user_id']))
    conn.commit()
    cur.close()
    conn.close()

    flash("Evaluación eliminada correctamente.", "info")
    return redirect(url_for('profesor.profesor_detalle', id=id_profesor))
