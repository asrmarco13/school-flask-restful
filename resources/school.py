from flask_restplus import Resource, Namespace
from models.school import SchoolModel


class School(Resource):
    api = Namespace('School flask restplus')

    @api.doc(responses={
        200: 'OK',
        404: 'Not found'
    })
    def get(self, name):
        school = SchoolModel.find_by_name(name)

        if school:
            return school.json()

        return {
            "message": "School not found"
        }, 404

    @api.doc(responses={
        201: 'Created',
        400: 'Bad Request',
        500: 'Internal Server Error'
    })
    def post(self, name):
        school = SchoolModel.find_by_name(name)

        if school:
            return {
                "message": "A school with name %s \
                already exists" % (name)
            }, 400

        school = SchoolModel(name)

        try:
            school.save_to_db()
        except Exception:
            return {
                "message": "An error occured creating \
                the school"
            }, 500

        return school.json()

    @api.doc(responses={
        200: 'OK'
    })
    def delete(self, name):
        school = SchoolModel.find_by_name(name)

        if school:
            school.delete_from_db()

        return {
            "message": "%s deleted" % (name)
        }
