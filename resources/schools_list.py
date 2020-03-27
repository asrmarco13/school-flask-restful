from flask_restplus import Resource
from models.school import SchoolModel
from flask_jwt_extended import jwt_optional, get_jwt_identity
import constants


class SchoolsList(Resource):
    @jwt_optional
    @classmethod
    def get(cls):
        username = get_jwt_identity()
        schools = [school.json() for school in SchoolModel.find_all()]
        if username:
            return {"schools": schools}, 200

        return (
            {
                "schools": [school["name"] for school in schools],
                "message": constants.MORE_DATA_AVAILABLE,
            },
            200,
        )
