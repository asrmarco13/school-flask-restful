import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']

        if UserModel.find_by_username(username):
            return {"message": "Username already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
