from flask_restplus import Resource, Namespace
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
)


class TokenRefresh(Resource):
    api = Namespace("School flask restplus")

    @jwt_refresh_token_required
    @api.doc(responses={200: "OK"})
    @classmethod
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
