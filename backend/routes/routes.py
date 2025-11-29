from flask_restful import Api, Resource
from flask import request
from flask_caching import Cache

from models.models import db, User, Role, Patient

cache = Cache()
api=Api()

class helloWorld(Resource):
    def get(self):
        return {"data":"hello world"}

api.add_resource(helloWorld, '/')

# {
#     "full_name" : "Tayyab",
#     "email" : "tayyab@123",
#     "password" : "pass@123",
#     "mobile_no" : "734*******"
# }

class Registration(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'full_name' in data or 'email' in data or 'passowrd' in data or 'mobile_no' in data:
            return{'message' : 'Fill all required fields'} , 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'message' : 'User already exist, try another email'} , 409



        new_user = User(full_name=data['full_name'], email=data['email'], password_hash=data['password'], mobile_no=data['mobile_no'])
        new_patient = Patient()
        patient_role = Role.query.filter_by(name='Patient').first()

        new_user.patient_profile = new_patient
        new_user.role.append(patient_role)
        
        db.session.add(new_patient)
        db.session.commit()
        return {'message' : 'User registered successfully!'} , 201
api.add_resource(Registration, '/register')

class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return{"message": "Enter the fields"}, 400
        if not data['email']:
            return{"message": "Enter your email"}, 400
        if not data['password']:
            return{"message": "Enter your password"}, 400
        
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return{"message": "Enter a valid Email"}, 401
        if not User.check_password(data['password']):
            return{"message": "Password incorrect"}, 401
        else:
            return{"message": "Login Successful"}, 200
    
api.add_resource(Login, '/login')