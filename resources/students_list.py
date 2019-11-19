from flask_restplus import Resource
from models.student import StudentModel


class StudentsList(Resource):
    def get(self):
        return {
            "students": [student.json() for student in StudentModel.query.all()]
        }
