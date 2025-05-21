from .auth_routes import auth_bp
from .profesor_routes import profesor_bp
from .evaluacion_routes import evaluacion_bp
from .main_routes import main_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(profesor_bp)
    app.register_blueprint(evaluacion_bp)
    app.register_blueprint(main_bp)
