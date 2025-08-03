from flask_sqlalchemy import SQLAlchemy #ORM que vamos a estar utilizando. Tanto la documentacion general de SQLAlchemy y la especifica relacionada con flask aplican
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__= True
    id = db.Column(db.Integer, primary_key=True) #Cualquier Int PK es tomado directamente como Autoincremental
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_deleted = db.Column(db.DateTime, nullable=True)

#Las definiciones de tablas Muchos a Muchos tienen que ser definidas PREVIO a las clases. SQLAlchemy toma un enfoque mas a menos
user_course = db.Table(
    "user_course", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id", ondelete="CASCADE"), primary_key=True)
)

class AcademicLevel(BaseModel):
    __tablename__ = "academiclevel"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    #Relacion uno a muchos con User. Importante, el primer argumento es el nombre de la CLASE, no la TABLA. El segundo argumento es el nombre de la columna en la tabla del otro lado.
    users = db.relationship("User", back_populates="level")
    #Esta funcion es necesaria para generar la estructura que sera devuelta en un JSON, sino no se pueden resolver los tipos. Va a ser necesaria en todas las clases
    def to_dict(self, include_users=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created,
            "date_deleted": self.date_deleted,
        }
        if include_users: #La query popula todas las relaciones, por temas de largo y posibles bucles, aclaramos si necesitamos mostrar los muchos o no
            data["users"] = [user.to_dict() for user in self.users]
        return data

class Course(BaseModel):
    __tablename__ = "course"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    users = db.relationship(
        "User", #nombre de la CLASE
        secondary=user_course, #El secondary indica la tabla intermedia en la base de datos, que tiene que ser definida previamente
        back_populates="courses" #nombre de la COLUMNA en la clase
    )

    def to_dict(self, include_users=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created,
            "date_deleted": self.date_deleted,
        }
        if include_users: #La query popula todas las relaciones, por temas de largo y posibles bucles, aclaramos si necesitamos mostrar los muchos o no
            data["users"] = [user.to_dict() for user in self.users]
        return data


class User(BaseModel):
    __tablename__ = "user"

    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    level_id = db.Column(db.Integer, db.ForeignKey("academiclevel.id", ondelete="CASCADE"), nullable=False) #Por mas que defina la relacion, tambien tengo que definir la columna del lado del muchos
    level = db.relationship("AcademicLevel", back_populates="users")  

    courses = db.relationship( 
        "Course",
        secondary=user_course,
        back_populates="users"
    )
    def to_dict(self, include_level=False):
        data = {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "level_id": self.level_id
        }
        if include_level and self.level: #mostramos los datos del nivel del usuario
            data["level"] = self.level.to_dict() 
        return data


