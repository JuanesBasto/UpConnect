from flask import Flask

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Importar blueprint aquí para evitar problema de importación circular
from app.routes import main
app.register_blueprint(main)
