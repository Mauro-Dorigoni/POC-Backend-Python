from flask import Blueprint, request, jsonify
from models import db,AcademicLevel,User
import datetime

user_bp = Blueprint("user_bp",__name__)

@user_bp.route("/user",methods=["POST"])
def create_user():
    data = request.json
    name = data["name"]
    lastname = data["lastname"]
    email = data["email"]
    level_id = data.get("level",{}).get("id")
    level = AcademicLevel.query.get_or_404(level_id)
    user = User(name=name,lastname=lastname,email=email,level=level)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"User added","id":user.id}),201