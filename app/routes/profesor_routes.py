# app/routes/profesor_routes.py
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.models.profesor_models import (
    obtener_profesor_por_slug, obtener_materias_por_profesor, obtener_total_evaluaciones, obtener_evaluaciones_paginadas, obtener_promedio_estrellas, listar_profesores_con_promedio)

profesor_bp = Blueprint('profesor', __name__)

@profesor_bp.route('/profesores/<slug>')
def profesor_detalle(slug):
    if 'user_id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('auth.login'))

    page = int(request.args.get('page', 1))
    per_page = 3
    offset = (page - 1) * per_page

    profesor = obtener_profesor_por_slug(slug)
    if not profesor:
        flash("Profesor no encontrado", "warning")
        return redirect(url_for('main.dashboard'))

    id_profesor = profesor['ID_profesor']
    materias = obtener_materias_por_profesor(id_profesor)
    total_eval = obtener_total_evaluaciones(id_profesor)
    total_pages = (total_eval + per_page - 1) // per_page
    evaluaciones = obtener_evaluaciones_paginadas(id_profesor, per_page, offset)
    promedio = obtener_promedio_estrellas(id_profesor) if total_eval > 0 else None

    return render_template('profesor_detalle.html',
                           profesor=profesor,
                           slug=slug,
                           materias=materias,
                           evaluaciones=evaluaciones,
                           promedio=promedio,
                           page=page,
                           total_pages=total_pages)

@profesor_bp.route('/profesores')
def listar_profesores():
    profesores = listar_profesores_con_promedio()
    return render_template('profesores_lista.html', profesores=profesores)
