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
from resources.token_refresh import TokenRefresh

app = Flask(__name__)
app.config['DEBUG'] = True

# if env DATABASE_URL not found use default sqlite schema
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///school.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
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
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=8080)
