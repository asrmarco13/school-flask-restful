from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required


class LogoutUser(Resource):
    api = Namespace("School flask restplus")

    @jwt_required
    @api.doc(responses={
        200: 'OK'
    })
    def post(self):
        return {
            "message": "User logout"
        }, 200
