from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection  # Importa aquí

main = Blueprint('main', __name__)

@main.route('/registro', methods=['GET', 'POST'])
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

    # Agrupar por facultad
    from collections import defaultdict
    carreras_por_facultad = defaultdict(list)

    for carrera in carreras_raw:
        carreras_por_facultad[carrera["nombre_facultad"]].append({
            "ID_carrera": carrera["ID_carrera"],
            "nombre_carrera": carrera["nombre_carrera"]
        })


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
            contrasena_hash = generate_password_hash(contrasena)
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
            """, (nombre, apellido, correo, contrasena_hash, semestre, semillero, id_carrera))

            
            conn.commit()
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('main.registro'))

        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template('register.html', carreras_por_facultad=carreras_por_facultad)

@main.route('/login', methods =['GET', 'POST'])
def login():
    if request.method=='POST':
        correo = request.form.get("correo")
        contrasena =  request.form.get("contrasena")

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Usuarios WHERE Correo_institucional = ? ", (correo,))
        usuario = cur.fetchone()
        
        if usuario and check_password_hash(usuario["Contrasena"], contrasena):
            session["usuario"] = correo
            flash("inicio de sesion exitoso", "success")
            return redirect(url_for("main.dashboard")) #redirecciona al panel
        else:
            flash("Correo o contraseña incorrectos", "danger")
    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("main.login"))


@main.route("/dashboard")
def dashboard():
    if "usuario" in session:
        return render_template("dashboard.html")
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("main.login"))

@main.route('/profesores/<int:id>')
def profesor_detalle(id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Consulta datos del profesor junto con facultad (si tienes relación)
    cur.execute("""
        SELECT p.ID_profesor, p.Nombre AS nombre_profesor, f.Nombre AS nombre_facultad
        FROM Profesores p
        LEFT JOIN Facultades f ON p.ID_facultad = f.ID_facultad
        WHERE p.ID_profesor = %s
    """, (id,))
    profesor = cur.fetchone()

    if not profesor:
        flash("Profesor no encontrado", "warning")
        return redirect(url_for('main.dashboard'))

    # Consulta materias que dicta el profesor
    cur.execute("""
        SELECT m.Nombre AS nombre_materia
        FROM Materias m
        INNER JOIN profesores_materias pm ON m.ID_materia = pm.ID_materia
        WHERE pm.ID_profesor = %s
    """, (id,))
    materias = cur.fetchall()

    # Consulta evaluaciones
    cur.execute("""
        SELECT Estrellas, Comentario, Fecha
        FROM Evaluaciones
        WHERE ID_profesor = %s
        ORDER BY Fecha DESC
    """, (id,))
    evaluaciones = cur.fetchall()

    cur.close()
    conn.close()

    # Calcular promedio de calificaciones si hay evaluaciones
    promedio = None
    if evaluaciones:
        promedio = sum(e['Calificacion'] for e in evaluaciones) / len(evaluaciones)

    return render_template('profesor_detalle.html', profesor=profesor, materias=materias, evaluaciones=evaluaciones, promedio=promedio)
