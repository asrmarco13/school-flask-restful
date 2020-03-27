from flask_restplus import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity
from models.student import StudentModel
import constants


class StudentsList(Resource):
    @jwt_optional
    def get(self):
        user_username = get_jwt_identity()
        students = [student.json() for student in StudentModel.find_all()]
        if user_username:
            return {"students": students}, 200

        return (
            {
                "students": [student["name"] for student in students],
                "message": constants.MORE_DATA_AVAILABLE,
            },
            200,
        )
