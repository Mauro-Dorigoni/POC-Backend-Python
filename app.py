from flask import Flask #API REST en Python
from models import db
from academiclevel_controller import level_bp
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

env_name = os.getenv("ENVIRONMENT", "development")

if env_name == "production":
    load_dotenv(".env.production")
elif env_name == "testing":
    load_dotenv(".env.testing")
else:
    load_dotenv(".env.development")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = Flask(__name__)
#Configuracion de la BD
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Es un modo debug del ORM por consola, potencialmente util pero molesto por lo cual de momento lo dejo desactivado


db.init_app(app) #Inicializa las configuraciones de la app Flask
app.register_blueprint(level_bp) #Agrega las Rutas definidas en el controlador de Level

#Inicializa la API en el puerto especificado al ser llamado este archivo por consola
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)