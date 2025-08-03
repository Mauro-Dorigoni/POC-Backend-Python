from flask import Blueprint, request, jsonify
from models import db,AcademicLevel,User,Course

course_bp = Blueprint("course_bp",__name__)

@course_bp.route("/course",methods=["POST"])
def create_course():
    data = request.json
    name = data["name"]
    description = data["description"]
    course = Course(name=name,description=description)
    db.session.add(course)
    db.session.commit()
    return jsonify({"message":"Course added","id":course.id}),201

@course_bp.route("/course", methods=["GET"])
def get_all_courses():
    courses = Course.query.all()
    return jsonify({
    "message": "Courses found",
    "courses": [course.to_dict(include_users=True) for course in courses]
    }), 200