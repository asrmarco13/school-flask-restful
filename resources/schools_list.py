from flask_restful import Resource
from models.school import SchoolModel


class SchoolsList(Resource):
    def get(self):
        return {
            "schools": [school.json() for school in SchoolModel.query.all()]
        }
