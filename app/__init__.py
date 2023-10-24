from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

mail = Mail()

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login_page'
loginManager.login_message = 'Please Login'
loginManager.login_message_category = 'danger'
    
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    
    from app.users.routes import users
    from app.main.routes import main
    from app.posts.routes import posts
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)
    
    with app.app_context():
        db.create_all()
    
    return app