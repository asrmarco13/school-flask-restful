from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.student import StudentModel
import constants


class Student(Resource):
    api = Namespace("School flask restplus")

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help=constants.BLANK_ERROR.format("name")
    )
    parser.add_argument(
        "surname", type=str, required=True, help=constants.BLANK_ERROR.format("surname")
    )
    parser.add_argument(
        "age", type=int, required=True, help=constants.BLANK_ERROR.format("age")
    )
    parser.add_argument(
        "classroom",
        type=str,
        required=True,
        help=constants.BLANK_ERROR.format("classroom"),
    )
    parser.add_argument(
        "school_id", type=int, required=True, help=constants.SCHOOL_ID_REQUIRED
    )

    @jwt_required
    @api.doc(
        responses={
            200: "OK",
            401: "Unauthorized",
            403: "Not Authorized",
            404: "Not found",
        }
    )
    @classmethod
    def get(cls, identification_number: int):
        student = StudentModel.find_by_name_surname(identification_number)
        if student:
            return student.json()

        return {"message": constants.STUDENT_NOT_FOUND}, 404

    @api.doc(responses={201: "Created", 404: "Not found", 500: "Internal Server Error"})
    @api.expect(parser)
    @fresh_jwt_required
    @classmethod
    def post(cls, identification_number: int):
        student = StudentModel.find_by_name_surname(identification_number)
        if student:
            return (
                {"message": constants.STUDENT_EXISTS.format(identification_number)},
                400,
            )

        data = Student.parser.parse_args()
        student = StudentModel(identification_number, **data)

        try:
            student.save_to_db()
        except Exception:
            return {"message": constants.ERROR_INSERT_STUDENT}, 500

        return student.json(), 201

    @api.doc(responses={200: "OK", 500: "Internal Server Error"})
    @api.expect(parser)
    @classmethod
    def put(cls, identification_number: int):
        student = StudentModel.find_by_name_surname(identification_number)
        data = Student.parser.parse_args()

        if student is None:
            student = StudentModel(identification_number, **data)
        else:
            student.name = data["name"]
            student.surname = data["surname"]
            student.age = data["age"]
            student.classroom = data["classroom"]

        try:
            student.save_to_db()
        except Exception:
            return {"message": constants.ERROR_INSERT_STUDENT}, 500

        return student.json()

    @api.doc(responses={200: "OK"})
    @classmethod
    def delete(cls, identification_number: int):
        student = StudentModel.find_by_name_surname(identification_number)

        if student:
            student.delete_from_db()

        return {"message": constants.STUDENT_DELETED.format(identification_number)}
