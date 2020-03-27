from flask_restplus import Resource, Namespace
from models.school import SchoolModel
import constants


class School(Resource):
    api = Namespace("School flask restplus")

    @api.doc(responses={200: "OK", 404: "Not found"})
    def get(self, name: str):
        school = SchoolModel.find_by_name(name)

        if school:
            return school.json()

        return {"message": constants.SCHOOL_NOT_FOUND}, 404

    @api.doc(
        responses={201: "Created", 400: "Bad Request", 500: "Internal Server Error"}
    )
    def post(self, name: str):
        school = SchoolModel.find_by_name(name)

        if school:
            return {"message": constants.SCHOOL_EXISTS.format(name)}, 400

        school = SchoolModel(name)

        try:
            school.save_to_db()
        except Exception:
            return {"message": constants.SCHOOL_CREATE_ERROR}, 500

        return school.json()

    @api.doc(responses={200: "OK"})
    def delete(self, name: str):
        school = SchoolModel.find_by_name(name)

        if school:
            school.delete_from_db()

        return {"message": constants.SCHOOL_DELETED.format(name)}
