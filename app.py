import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.school import School
from resources.student import Student
from resources.schools_list import SchoolsList
from resources.students_list import StudentsList
from resources.user import UserRegister
from security import authenticate, identity


app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://nzfyemgfddgrdc:c28b27270e2e04286dbc8df6005493e4fb9f1a2369da4fdff58f00c87583e64d@ec2-54-247-92-167.eu-west-1.compute.amazonaws.com:5432/d3i897tq0ljc43')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "marco"
api = Api(app)

# /auth
jwt = JWT(app, authenticate, identity)

api.add_resource(School, '/school/<string:name>')
api.add_resource(Student, '/student')
api.add_resource(SchoolsList, '/schools')
api.add_resource(StudentsList, '/students')

api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=8080)
