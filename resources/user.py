from flask_restplus import Resource, reqparse, Namespace
from models.user import UserModel
import constants


class UserRegister(Resource):
    api = Namespace("School flask restplus")
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help=constants.BLANK_ERROR.format("username"),
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help=constants.BLANK_ERROR.format("password"),
    )

    @api.doc(responses={201: "Created", 400: "Bad Request"})
    @api.expect(parser)
    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()
        username = data["username"]

        if UserModel.find_by_username(username):
            return {"message": constants.USER_EXISTS}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": constants.USER_CREATED}, 201
