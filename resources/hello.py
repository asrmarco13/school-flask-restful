from flask_restplus import Resource


WELCOME_MESSAGE = "Welcome to my REST application deployed on Heroku"


class Hello(Resource):
    def get(self):
        return {"message": WELCOME_MESSAGE}
