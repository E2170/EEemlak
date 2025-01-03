import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # type: ignore

# Veritabanı ve oturum yönetimi için objeler
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Uygulama yapılandırması
    base_dir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(base_dir, 'EE-Emlak.db')  # Sabit veritabanı dosyası
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SECRET_KEY'] = 'ee_emlak_secret'

    
    db.init_app(app)

    
    from .routes import main
    app.register_blueprint(main)

    # Veritabanı tablolarını kontrol et ve oluştur
    with app.app_context():
        if not os.path.exists(database_path):  # Eğer veritabanı dosyası yoksa tablolar oluşturulacak
            db.create_all()

    return app
