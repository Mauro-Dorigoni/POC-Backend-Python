from app import app, db #Archivo para dar de alta las tablas
with app.app_context():
    db.create_all()
    print("Tablas creadas correctamente.")
