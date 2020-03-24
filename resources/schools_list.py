from flask_restplus import Resource
from models.school import SchoolModel
from flask_jwt_extended import jwt_optional, get_jwt_identity


class SchoolsList(Resource):
    @jwt_optional
    def get(self):
        username = get_jwt_identity()
        schools = [school.json() for school in SchoolModel.query.all()]
        if username:
            return {
                "schools": schools
            }, 200

        return {
            "schools": [school['name'] for school in schools],
            "message": "More data available if you log in"
        }, 200
