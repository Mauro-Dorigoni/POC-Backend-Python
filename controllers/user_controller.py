from flask import Blueprint, request, jsonify
from models import db,AcademicLevel,User,Course
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
    user = User(name=name,lastname=lastname,email=email,level=level) #Tambien se puede usar level_id=level_id, es indistinto y la relacion se poupula igual
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"User added","id":user.id}),201

@user_bp.route("/user/level/<int:level_id>", methods=["GET"])
def get_users_by_level(level_id):
    level = AcademicLevel.query.get_or_404(level_id)
    users = User.query.filter_by(level_id=level.id).all() #Ejemplo de un filtro en una consulta, pueden ir tantos argumentos como quieran  
    return jsonify({
        "users": [user.to_dict(include_level=True) for user in users]
    }), 200

@user_bp.route("/user/<int:user_id>/enroll", methods=["POST"])
def enroll_user_in_courses(user_id): #Ejemplo del caso de uso de inscripcion simultanea a mas de un curso. Mando un json con un array de ids de curso
    user = User.query.get_or_404(user_id)
    data = request.json
    course_ids = data.get("course_ids", [])
    if not course_ids:
        return jsonify({"error": "No course_ids provided"}), 400
    courses = Course.query.filter(Course.id.in_(course_ids)).all()
    if len(courses) != len(course_ids):
        return jsonify({"error": "One or more courses not found"}), 404
    for course in courses:
        if course not in user.courses:
            user.courses.append(course)
    db.session.commit()
    return jsonify({
        "message": f"User {user.name} enrolled in {len(courses)} courses",
        "courses": [ {"id": c.id, "title": c.name} for c in user.courses ]
    }), 200

