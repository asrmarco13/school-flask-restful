from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
from models.user import UserModel
import constants


class LoginUser(Resource):
    api = Namespace("School flask restplus")

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        required=True,
        type=str,
        help=constants.BLANK_ERROR.format("username"),
    )

    parser.add_argument(
        "password",
        required=True,
        type=str,
        help=constants.BLANK_ERROR.format("password"),
    )

    @api.doc(responses={200: "OK", 400: "Bad Request", 404: "Not Found"})
    @api.expect(parser)
    @classmethod
    def post(cls):
        data = LoginUser.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            username = user.username
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(username)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": constants.INVALID_CREDENTIALS}, 401
