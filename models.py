from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__= True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_deleted = db.Column(db.DateTime, nullable=True)

user_course = db.Table(
    "user_course", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"), primary_key=True)
)

class AcademicLevel(BaseModel):
    __tablename__ = "academiclevel"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    users = db.relationship("User", back_populates="level")
    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "date_created":self.date_created,
            "date_deleted":self.date_deleted
        }

class Course(BaseModel):
    __tablename__ = "course"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    users = db.relationship(
        "User",
        secondary=user_course,
        back_populates="courses"
    )

class User(BaseModel):
    __tablename__ = "user"

    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    level_id = db.Column(db.Integer, db.ForeignKey("academiclevel.id", ondelete="CASCADE"), nullable=False)
    level = db.relationship("AcademicLevel", back_populates="users")  

    courses = db.relationship( 
        "Course",
        secondary=user_course,
        back_populates="users"
    )


