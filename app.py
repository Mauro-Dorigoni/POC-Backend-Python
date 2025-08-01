from flask import Flask
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
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(level_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)