# __init__.py
from flask import Flask
from .extensions import db, bcrypt
from flask_login import LoginManager
from .models import User
import os

# Inicializar o objeto LoginManager fora da função
login_manager = LoginManager()

# Função que carrega o usuário com base no ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_key')  # Use variável de ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configurar redirecionamento para login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Inicializar extensões
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Importar e registrar blueprints
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    # Inicializar banco de dados
    with app.app_context():
        db.create_all()

    return app
