from typing import Dict, List, Union
from db import db
from models.student import StudentJSON


SchoolJSON = Dict[str, Union[str, List[StudentJSON]]]


class SchoolModel(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    students = db.relationship("StudentModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> SchoolJSON:
        return {
            "name": self.name,
            "students": [student.json() for student in self.students.all()],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "SchoolModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls) -> List["SchoolModel"]:
        return cls.query.all()
