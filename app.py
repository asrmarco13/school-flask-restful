import os

from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from resources.school import School
from resources.student import Student
from resources.schools_list import SchoolsList
from resources.students_list import StudentsList
from resources.user import UserRegister
from resources.hello import Hello
from resources.login import LoginUser

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://nzfyemgfddgrdc:c28b27270e2e04286dbc8df6005493e4fb9f1a2369da4fdff58f00c87583e64d@ec2-54-247-92-167.eu-west-1.compute.amazonaws.com:5432/d3i897tq0ljc43')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTPLUS_VALIDATE'] = True
app.config['JWT_SECRET_KEY'] = "marco"
api = Api(
    app=app,
    description="API school-flask-restplus",
    default="School flask restplus"
)

jwt = JWTManager(app)

api.add_resource(LoginUser, '/login')
api.add_resource(School, '/school/<string:name>')
api.add_resource(Student, '/student/<string:identification_number>')
api.add_resource(SchoolsList, '/schools')
api.add_resource(StudentsList, '/students')

api.add_resource(UserRegister, '/register')

api.add_resource(Hello, '/hello')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=8080)
