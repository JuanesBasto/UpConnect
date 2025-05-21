from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection
from app.utils.validators import correo_institucional_valido
from collections import defaultdict

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.ID_carrera, c.Nombre AS nombre_carrera, f.Nombre AS nombre_facultad
        FROM Carreras c
        JOIN Facultades f ON c.ID_facultad = f.ID_facultad
        ORDER BY f.Nombre, c.Nombre
    """)
    carreras_raw = cur.fetchall()
    carreras_por_facultad = defaultdict(list)

    for carrera in carreras_raw:
        carreras_por_facultad[carrera["nombre_facultad"]].append({
            "ID_carrera": carrera["ID_carrera"],
            "nombre_carrera": carrera["nombre_carrera"]
        })

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

        try:
            cur.execute("SELECT * FROM Usuarios WHERE Correo_institucional = ?", (correo,))
            if cur.fetchone():
                flash("El correo ya está registrado", "danger")
                return redirect(url_for("auth.registro"))

            contrasena_hash = generate_password_hash(contrasena)
            cur.execute("""
                INSERT INTO Usuarios (Nombre, Apellido, Correo_institucional, Contrasena, Fecha_registro, Semestre, Semillero, ID_carrera)
                VALUES (?, ?, ?, ?, CURDATE(), ?, ?, ?)
            """, (nombre, apellido, correo, contrasena_hash, semestre, semillero, id_carrera))
            conn.commit()
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template('register.html', carreras_por_facultad=carreras_por_facultad)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Usuarios WHERE Correo_institucional = ?", (correo,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()

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
