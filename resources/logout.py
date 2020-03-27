from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_raw_jwt
from blacklist import BLACKLIST
import constants


class LogoutUser(Resource):
    api = Namespace("School flask restplus")

    @jwt_required
    @api.doc(responses={200: "OK"})
    @classmethod
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": constants.USER_LOGOUT}, 200
