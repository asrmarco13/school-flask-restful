from flask_restplus import Resource
import constants


class Hello(Resource):
    @classmethod
    def get(cls):
        return {"message": constants.WELCOME_MESSAGE}
