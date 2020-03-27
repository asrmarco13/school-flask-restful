from flask_restplus import Resource
import constants


class Hello(Resource):
    def get(self):
        return {"message": constants.WELCOME_MESSAGE}
