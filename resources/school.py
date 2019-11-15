from flask_restful import Resource
from models.school import SchoolModel


class School(Resource):
    def get(self, name):
        school = SchoolModel.find_by_name(name)

        if school:
            return school.json()

        return {
            "message": "School not found"
        }, 404

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

    def delete(self, name):
        school = SchoolModel.find_by_name(name)

        if school:
            school.delete_from_db()

        return {
            "message": "%s deleted" % (name)
        }
