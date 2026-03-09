from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.models import db, User, Role, Patient

class Register(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['email', 'password', 'full_name', 'mobile_no', 'age', 'gender']
        if not all(i in data for i in required_fields):
            return {'message': 'Missing fields'}, 400
            
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 409

        new_user = User(full_name=data['full_name'], email=data['email'], mobile_no=data['mobile_no'])
        new_user.set_password(data['password'])
        
        patient_role = Role.query.filter_by(name='Patient').first()
        if patient_role: new_user.roles.append(patient_role)

        new_patient = Patient(age=data['age'], gender=data['gender'])
        new_user.patient_profile = new_patient

        db.session.add(new_user)
        db.session.add(new_patient)
        db.session.commit()
        return {'message': 'Patient registered successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()

        if user and user.check_password(data.get('password')):
            role = user.roles[0].name if user.roles else 'Patient'
            access_token = create_access_token(identity=str(user.id), additional_claims={'role': role})
            
            return {
                'message': 'Login Successful',
                'access_token': access_token,
                'role': role,
                'user_id': user.id,
                'full_name': user.full_name  # <--- ADDED THIS LINE
            }, 200

        return {'message': 'Invalid credentials'}, 401