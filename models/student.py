from typing import Dict, List, Union
from db import db

StudentJSON = Dict[str, Union[int, str]]


class StudentModel(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    age = db.Column(db.Integer)
    classroom = db.Column(db.String(10))

    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"))
    school = db.relationship("SchoolModel")

    def __init__(
        self,
        identification_number: int,
        name: str,
        surname: str,
        age: int,
        classroom: str,
        school_id: int,
    ):
        self.id = identification_number
        self.name = name
        self.surname = surname
        self.age = age
        self.classroom = classroom
        self.school_id = school_id

    def json(self) -> StudentJSON:
        return {
            "identification number": self.id,
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "classroom": self.classroom,
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name_surname(cls, identification_number: int) -> "StudentModel":
        return cls.query.filter_by(id=identification_number).first()

    @classmethod
    def find_all(cls) -> List["StudentModel"]:
        return cls.query.all()
