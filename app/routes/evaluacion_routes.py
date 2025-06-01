from flask import Blueprint, request, redirect, session, url_for, flash
from datetime import datetime
from app.models.evaluacion_models import (ya_evaluo, insertar_evaluacion, actualizar_evaluacion, eliminar_evaluacion)



evaluacion_bp = Blueprint('evaluacion', __name__)

@evaluacion_bp.route('/evaluar/<int:id>', methods=['POST'])
def agregar_evaluacion(id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    estrellas = int(request.form['estrellas'])
    comentario = request.form.get('comentario') or ''

    if not (1 <= estrellas <= 5):
        flash("La calificación debe estar entre 1 y 5", "danger")
        return redirect(url_for('profesor.profesor_detalle', slug=id))

    if ya_evaluo(id, user_id):
        flash("Ya has evaluado a este profesor", "warning")
        return redirect(url_for('profesor.profesor_detalle', slug=id))

    insertar_evaluacion(id, user_id, estrellas, comentario)
    flash("¡Gracias por tu evaluación!", "success")
    return redirect(url_for('profesor.profesor_detalle', slug=id))

@evaluacion_bp.route('/evaluaciones/editar_ajax/<int:id_evaluacion>', methods=['POST'])
def editar_evaluacion_ajax(id_evaluacion):
    if 'user_id' not in session:
        return {'success': False, 'message': 'No autenticado'}, 401

    data = request.get_json()
    estrellas = data.get('estrellas')
    comentario = data.get('comentario')

    actualizar_evaluacion(id_evaluacion, session['user_id'], estrellas, comentario)
    flash("¡Evaluación actualizada!", "success")
    return {'success': True, 'message': 'Evaluación actualizada'}

@evaluacion_bp.route('/evaluaciones/eliminar/<int:id_profesor>', methods=["POST"])
def eliminar_evaluacion_route(id_profesor):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    eliminar_evaluacion(id_profesor, session['user_id'])
    flash("Evaluación eliminada correctamente.", "info")
    return redirect(url_for('profesor.profesor_detalle', slug=id_profesor))
