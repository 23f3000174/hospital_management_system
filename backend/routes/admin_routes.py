from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models.models import db, User, Doctor, Patient, Appointment, Role, Department

def is_admin():
    claims = get_jwt()
    return claims['role'] == 'Admin'

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        return {
            'total_doctors': Doctor.query.count(),
            'total_patients': Patient.query.count(),
            'total_appointments': Appointment.query.count()
        }

class ManageDepartment(Resource):
    @jwt_required()
    def get(self):
        depts = Department.query.all()
        return [
            {'id': d.id, 'name': d.department_name, 'description': d.description} for d in depts
        ], 200
    
    @jwt_required()
    def post(self):
        if not is_admin(): return {'message':'Unauthorized'}, 403 
        data = request.get_json()

        if Department.query.filter_by(department_name=data['department_name']).first():
            return {'message': 'Department already exists'}, 400

        new_dept = Department(department_name=data['department_name'], description=data['description'])
        db.session.add(new_dept)
        db.session.commit()
        return {"message": "New Department Added"}, 201

    @jwt_required()
    def delete(self, department_id=None):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        dept = Department.query.get_or_404(department_id)
        
        if Doctor.query.filter_by(department_id=department_id).first():
            return {'message': 'Cannot delete: Doctors are assigned to this department.'}, 400
        
        try:
            db.session.delete(dept)
            db.session.commit()
            return {'message': 'Department deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class ManageDoctor(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        doctors = Doctor.query.all()
        data = []
        for d in doctors:
            data.append({
                'id': d.id, 
                'full_name': d.user.full_name,
                'email': d.user.email,
                'medical_id': d.medical_id,
                'department': d.department.department_name,
                'status': d.user.flag
            })
        return data, 200
    
    @jwt_required()
    def post(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        new_user = User(
            full_name=data['full_name'],
            email=data['email'],
            mobile_no=data['mobile_no']
        )
        new_user.set_password(data['password'])
        
        doctor_role = Role.query.filter_by(name='Doctor').first()
        new_user.roles.append(doctor_role)

        dept = Department.query.filter_by(department_name=data['department_name']).first()
        if not dept:
            return {'message': 'Department not found'}, 404

        new_doctor = Doctor(medical_id=data['medical_id'], department_id=dept.id)
        new_user.doctor_profile = new_doctor

        db.session.add(new_user)
        db.session.add(new_doctor)
        db.session.commit()
        return {'message': 'Doctor added successfully'}, 201

    @jwt_required()
    def put(self, doctor_id=None):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        user = User.query.get_or_404(doctor_id)
        data = request.get_json()
        if 'flag' in data:
            user.flag = data['flag']
            db.session.commit()
            return {'message': f'Status updated to {user.flag}'}, 200
        return {'message': 'No flag provided'}, 400

    @jwt_required()
    def delete(self, doctor_id=None):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        doctor = Doctor.query.get_or_404(doctor_id)
        user = User.query.get_or_404(doctor_id)
        try:
            db.session.delete(doctor)
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Doctor removed successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting doctor: {str(e)}'}, 500

class ManagePatient(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        patients = Patient.query.all()
        data = []
        for p in patients:
            data.append({
                'id': p.id, 
                'full_name': p.user.full_name,
                'email': p.user.email,
                'mobile_no': p.user.mobile_no,
                'age': p.age,
                'gender': p.gender,
                'flag': p.user.flag
            })
        return data, 200

    @jwt_required()
    def put(self, patient_id=None):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        user = User.query.get_or_404(patient_id)
        data = request.get_json()
        if 'flag' in data:
            user.flag = data['flag']
            db.session.commit()
            return {'message': f'Status updated to {user.flag}'}, 200
        return {'message': 'No flag provided'}, 400

    @jwt_required()
    def delete(self, patient_id=None):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        patient = Patient.query.get_or_404(patient_id)
        user = User.query.get_or_404(patient_id)
        try:
            db.session.delete(patient)
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Patient removed successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting patient: {str(e)}'}, 500