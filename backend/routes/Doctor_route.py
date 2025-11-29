from flask_restful import Api, Resource
from flask import request

from models.models import db, User, Doctor, Department
from .utils import pass_gen

class Doctor_routes(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'full_name' in data or 'email' in data or 'mobile_no' in data or 'medical_id' in data or 'availability' in data:
            return{'message' : 'Enter all required fields'} , 400
        
        password = pass_gen(20)
        new_user = User(full_name=data['full_name'], email=data['email'], password_hash=password, mobile_no=data['mobile_no'])

        department_id = Department.query.filter_by(department_name=data).first().id
        new_doctor = Doctor(medical_id=data['medical_id'], department_id=department_id)
