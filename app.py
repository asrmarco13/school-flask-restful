import os

from flask import Flask, jsonify
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from resources.school import School
from resources.student import Student
from resources.schools_list import SchoolsList
from resources.students_list import StudentsList
from resources.user import UserRegister
from resources.hello import Hello
from resources.login import LoginUser
from resources.token_refresh import TokenRefresh
from resources.logout import LogoutUser
from blacklist import BLACKLIST

app = Flask(__name__)
app.config["DEBUG"] = True

# if env DATABASE_URL not found use default sqlite schema
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///school.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["RESTPLUS_VALIDATE"] = True
app.config["JWT_SECRET_KEY"] = "marco"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
api = Api(
    app=app, description="API school-flask-restplus", default="School flask restplus"
)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"description": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"description": "Invalid token", "error": "invalid_token"}), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return (
        jsonify(
            {
                "description": "Request not contains \
        an access token",
                "error": "unauthorized_token",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return (
        jsonify({"description": "Token is not fresh", "error": "fresh_token_required"}),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify({"description": "Token has been revoked", "error": "token_revoked"}),
        401,
    )


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(LoginUser, "/login")
api.add_resource(School, "/school/<string:name>")
api.add_resource(Student, "/student/<string:identification_number>")
api.add_resource(SchoolsList, "/schools")
api.add_resource(StudentsList, "/students")
api.add_resource(UserRegister, "/register")
api.add_resource(Hello, "/hello")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(LogoutUser, "/logout")

if __name__ == "__main__":
    from db import db

    db.init_app(app)

    if app.config["DEBUG"]:

        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=8080)
