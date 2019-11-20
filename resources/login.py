from flask import request
from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import jwt_required, create_access_token
from security import authenticate

class LoginUser(Resource):
    api = Namespace("School flask restplus")

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        required=True,
        type=str,
        help='Username cannot be blank'
    )

    parser.add_argument(
        'password',
        required=True,
        type=str,
        help='Password cannot be blank'
    )

    @api.doc(responses={
        200: 'OK',
        400: 'Bad Request',
        404: 'Not Found'
    })
    @api.expect(parser)
    def post(self):
        data = LoginUser.parser.parse_args()
        user = authenticate(
            data['username'],
            data['password']
        )

        if not user:
            return {
                "message": "User not found"
            }, 404

        username = user.username
        access_token = create_access_token(identity=username)
        return {
            "access_token": access_token
        }, 200
