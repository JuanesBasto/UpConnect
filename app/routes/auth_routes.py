from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validators import correo_institucional_valido
from app.models.usuario_models import (obtener_carreras_por_facultad, buscar_usuario_por_correo, registrar_usuario)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    carreras_por_facultad = obtener_carreras_por_facultad()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        semestre = request.form['semestre']
        semillero = request.form['semillero']
        id_carrera = request.form['id_carrera']

        if not correo_institucional_valido(correo):
            flash("El correo debe ser institucional (@unipamplona.edu.co)", "danger")
            return redirect(url_for('auth.registro'))

        if buscar_usuario_por_correo(correo):
            flash("El correo ya está registrado", "danger")
            return redirect(url_for("auth.registro"))
        
        try:
            registrar_usuario(nombre, apellido, correo, contrasena, semestre, semillero, id_carrera)
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template('register.html', carreras_por_facultad=carreras_por_facultad)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = buscar_usuario_por_correo(correo)

        if usuario and check_password_hash(usuario['Contrasena'], contrasena):
            session['user_id'] = usuario['ID_usuario']
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("auth.login"))
