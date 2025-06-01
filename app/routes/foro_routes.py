
from flask import Blueprint, render_template, request
from app.models.foro_models import obtener_foros_por_materia, obtener_publicaciones_por_foro, obtener_foro_por_id

foro_bp = Blueprint('foro', __name__)

@foro_bp.route('/materias/<int:id_materia>/foros')
def ver_foros(id_materia):
    foros = obtener_foros_por_materia(id_materia)
    return render_template('foros/lista_foros.html', foros=foros, id_materia=id_materia)


@foro_bp.route('/foros/<int:id_foro>')
def ver_publicaciones(id_foro):
    foro = obtener_foro_por_id(id_foro)
    publicaciones = obtener_publicaciones_por_foro(id_foro)
    return render_template('foros/publicaciones.html', foro=foro, publicaciones=publicaciones)
