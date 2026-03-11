from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models.models import db, User, Doctor, Patient, Appointment, Role, Department, Treatment
from datetime import date
from routes import cache

def is_admin():
    claims = get_jwt()
    return claims['role'] == 'Admin'

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        cached = cache.get('admin_dashboard')
        if cached:
            return cached
        result = {
            'total_doctors': Doctor.query.count(),
            'total_patients': Patient.query.count(),
            'total_appointments': Appointment.query.count()
        }
        cache.set('admin_dashboard', result, timeout=30)
        return result

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
        cache.delete('department_list')
        cache.delete('admin_dashboard')
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
            cache.delete('department_list')
            cache.delete('admin_dashboard')
            return {'message': 'Department deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class ManageDoctor(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        q = request.args.get('q', '').lower()
        doctors = Doctor.query.all()
        data = []
        for d in doctors:
            if q and q not in d.user.full_name.lower() and q not in d.department.department_name.lower():
                continue
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
        cache.delete('admin_dashboard')
        
        from celery_app import send_doctor_welcome_email
        send_doctor_welcome_email.delay(data['email'], data['password'], data['full_name'])
        
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
            cache.delete('admin_dashboard')
            return {'message': 'Doctor removed successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting doctor: {str(e)}'}, 500

class ManagePatient(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        q = request.args.get('q', '').lower()
        patients = Patient.query.all()
        data = []
        for p in patients:
            if q and q not in p.user.full_name.lower() and q not in str(p.id) and q not in p.user.mobile_no:
                continue
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
            cache.delete('admin_dashboard')
            return {'message': 'Patient removed successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting patient: {str(e)}'}, 500

class AdminAppointments(Resource):
    @jwt_required()
    def get(self):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        status_filter = request.args.get('status', '').lower()
        today = date.today()
        appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.start_time.desc()).all()
        data = []
        for a in appointments:
            if status_filter == 'upcoming' and (a.date < today or a.status != 'Booked'):
                continue
            if status_filter == 'past' and a.date >= today:
                continue
            if status_filter in ['booked', 'completed', 'cancelled'] and a.status.lower() != status_filter:
                continue
            treatment = Treatment.query.filter_by(appointment_id=a.id).first()
            data.append({
                'id': a.id,
                'doctor_name': a.doctor.user.full_name,
                'patient_name': a.patient.user.full_name,
                'patient_id': a.patient_id,
                'date': str(a.date),
                'start_time': str(a.start_time),
                'status': a.status,
                'diagnosis': treatment.diagnosis if treatment else None,
                'prescription': treatment.prescription if treatment else None,
                'notes': treatment.notes if treatment else None
            })
        return data, 200

class AdminPatientHistory(Resource):
    @jwt_required()
    def get(self, patient_id):
        if not is_admin(): return {'message': 'Unauthorized'}, 403
        patient = Patient.query.get_or_404(patient_id)
        treatments = Treatment.query.join(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.status == 'Completed'
        ).all()
        history = []
        for t in treatments:
            history.append({
                'date': str(t.appointment.date),
                'doctor': t.appointment.doctor.user.full_name,
                'diagnosis': t.diagnosis,
                'prescription': t.prescription,
                'notes': t.notes
            })
        return {
            'patient_name': patient.user.full_name,
            'records': history
        }, 200