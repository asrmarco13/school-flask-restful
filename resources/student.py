from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'age',
        type=int,
        required=True,
        help="Age cannot be blank"
    )
    parser.add_argument(
        'classroom',
        type=str,
        required=True,
        help="Classroom cannot be blank"
    )
    parser.add_argument(
        'school_id',
        type=int,
        required=True,
        help="Every student needs a school id"
    )

    @jwt_required()
    def get(self):
        print(request.args)
        name = request.args.get('name')
        surname = request.args.get('surname')
        student = StudentModel.find_by_name_surname(name, surname)
        if student:
            return student.json()

        return {
            "message": "Student not found"
        }, 404

    def post(self):
        name = request.args.get('name')
        surname = request.args.get('surname')
        student = StudentModel.find_by_name_surname(name, surname)
        if student:
            return {
                "message": "A student with %s $s already exist"
                % (name, surname)
            }, 400

        data = Student.parser.parse_args()
        student = StudentModel(name, surname, **data)

        try:
            student.save_to_db()
        except Exception:
            return {
                "message": "An error occured inserting the student"
            }, 500

        return student.json(), 201

    def put(self):
        name = request.args.get('name')
        surname = request.args.get('surname')
        student = StudentModel.find_by_name_surname(name, surname)
        data = Student.parser.parse_args()

        if student is None:
            student = StudentModel(name, surname, **data)
        else:
            student.age = data['age']
            student.classroom = data['classroom']

        try:
            student.save_to_db()
        except Exception:
            return {
                "message": "An error occured inserting the student"
            }, 500

        return student.json()

    def delete(self):
        name = request.args.get('name')
        surname = request.args.get('surname')
        student = StudentModel.find_by_name_surname(name, surname)

        if student:
            student.delete_from_db()

        return {
            "message": "%s %s deleted"
            % (name, surname)
        }
