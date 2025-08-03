from flask import Blueprint, request, jsonify
from models import db,AcademicLevel
import datetime

level_bp=Blueprint("level_bp",__name__) #Un blueprint guarda las rutas y los metodos para que la API use

#CREATE
@level_bp.route("/level", methods=["POST"])
def create_level():
    data = request.json
    name = data["name"]
    description = data["description"]
    level=AcademicLevel(name=name,description=description)
    db.session.add(level) #Inicia la transaccion
    db.session.commit() #Commitea la transaccion
    return jsonify({"message":"Academic Level added","id":level.id}),201

#GETALL
@level_bp.route("/level", methods=["GET"])
def get_levels():
    levels = AcademicLevel.query.all() #Modo de hacer una Query a BD
    return jsonify({
    "message": "Academic Levels found",
    "levels": [level.to_dict(include_users=True) for level in levels]
    }), 200

#GETONE
@level_bp.route("/level/<int:id>",methods=["GET"])
def get_one_level(id):
    level = AcademicLevel.query.get_or_404(id) #El findOneOrFail de SQLAlchemy
    return jsonify({
        "message":"Academic Level Found",
        "level": level.to_dict(include_users=True)
    }),200

#DELETE (fisico)
@level_bp.route("/level/<int:id>",methods=["DELETE"])
def delete_level(id):
    level = AcademicLevel.query.get_or_404(id)
    db.session.delete(level)
    db.session.commit()
    return jsonify({"message": "Academic Level deleted successfully"}), 200

#UPDATE/BAJA LOGICA
@level_bp.route("/level/<int:id>",methods=["PATCH"])
def logic_delete_level(id):
    level = AcademicLevel.query.get_or_404(id)
    level.date_deleted = datetime.datetime.now()
    db.session.commit()
    return jsonify({"message": "Academic Level deleted (logically) successfully"}), 200
