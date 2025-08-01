from flask import Blueprint, request, jsonify
from models import db,AcademicLevel

level_bp=Blueprint("level_bp",__name__)

#CREATE
@level_bp.route("/level", methods=["POST"])
def create_level():
    data = request.json
    name = data["name"]
    description = data["description"]
    level=AcademicLevel(name=name,description=description)
    db.session.add(level)
    db.session.commit()
    return jsonify({"message":"Academic Level added","id":level.id}),201

#GETALL
@level_bp.route("/level", methods=["GET"])
def get_levels():
    levels = AcademicLevel.query.all()
    return jsonify({
    "message": "Academic Levels found",
    "levels": [level.to_dict() for level in levels]
    }), 201
