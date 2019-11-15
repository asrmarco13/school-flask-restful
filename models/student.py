from db import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    age = db.Column(db.Integer)
    classroom = db.Column(db.String(10))

    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    school = db.relationship('SchoolModel')

    def __init__(self, name, surname, age, classroom, school_id):
        self.name = name
        self.surname = surname
        self.age = age
        self.classroom = classroom
        self.school_id = school_id

    def json(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "classroom": self.classroom
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name_surname(cls, name, surname):
        return cls.query.filter_by(name=name, surname=surname).first()
