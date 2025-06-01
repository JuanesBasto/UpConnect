# UpConnect 🎓📡

**UpConnect** es una plataforma web desarrollada como proyecto académico en la Universidad de Pamplona. Su objetivo es conectar estudiantes con semilleros de investigación, docentes y recursos universitarios, facilitando el registro, autenticación y participación activa de los usuarios dentro del entorno académico.

---

## ⚙️ Tecnologías utilizadas

- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python (Flask)
- **Base de datos:** MariaDB
- **ORM / Seguridad:** Uso de hash para contraseñas, validación de correo institucional
- **Versionamiento:** Git + GitHub

---

## 🚀 Funcionalidades actuales

- Registro de usuarios con validación de dominio institucional `@unipamplona.edu.co`
- Inicio y cierre de sesión con manejo de sesiones seguras
- Inserción de datos en la base de datos (tablas relacionales con claves foráneas)
- Mensajes flash para retroalimentación del usuario
- Proyecto estructurado con Blueprints y conexión modular

---

## 📂 Estructura del proyecto

```
UpConnect/
│
├── app/
│ ├── init.py # Configuración e inicialización de la app
│ ├── db.py # Configuración de la base de datos
│ ├── routes.py # Definición de rutas y lógica del servidor
│ └── templates/ # Archivos HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
│
├── static/ # (por implementar) Estilos CSS, JS personalizados
│
├── app.py # Punto de entrada del servidor Flask
├── database.sql # Script de la base de datos
├── requirements.txt # Dependencias del entorno virtual
├── README.md # Documentación del proyecto
└── .gitignore # Archivos excluidos del control de versiones


---

## 🧪 Cómo ejecutar localmente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JuanesBasto/UpConnect.git
   cd upconnect

2. Activa el entorno virtual:

.\venv\Scripts\activate

3. Instala dependencias:
pip install -r requirements.txt

4. Ejecuta el servidor:
python app.py

5. Abre en el navegador: http://127.0.0.1:5000


📅 Progreso actual
Primera entrega: 21 de mayo de 2025
Estado: Módulo de autenticación funcional ✅
Siguiente objetivo: vista principal del panel de usuario y administración de datos..

🔐 Consideraciones
El correo institucional es obligatorio para registrarse.

Las contraseñas son almacenadas de forma segura con hash.

El proyecto es solo para fines académicos.

🧑‍💻 Autor
Juan Basto – Estudiante de Ingeniería de Sistemas, Universidad de Pamplona
