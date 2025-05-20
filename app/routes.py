from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection  # Importa aquí

main = Blueprint('main', __name__)

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_carrera, Nombre FROM Carreras")
    carreras = cur.fetchall()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        semestre = request.form.get('semestre')
        semillero = request.form.get('semillero')
        id_carrera = request.form.get('id_carrera')

        # Validar correo institucional
        if not correo.endswith("@unipamplona.edu.co"):
            flash("El correo debe ser institucional (@unipamplona.edu.co)", "danger")
            return redirect(url_for('main.registro'))

        try:
            # Verificar si el correo ya existe
            cur.execute("SELECT * FROM Usuarios WHERE Correo_institucional = ?", (correo,))
            usuario_existente = cur.fetchone()

            if usuario_existente:
                flash("El correo ya está registrado", "danger")
                return redirect(url_for("main.registro"))

            # Insertar si no existe
            cur.execute("""
                INSERT INTO Usuarios (
                    Nombre, Apellido, Correo_institucional, Contrasena, Fecha_registro,
                    Semestre, Semillero, ID_carrera
                )
                VALUES (?, ?, ?, ?, CURDATE(), ?, ?, ?)
            """, (nombre, apellido, correo, contrasena, semestre, semillero, id_carrera))

            
            conn.commit()
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('main.registro'))

        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template('register.html', carreras=carreras)
