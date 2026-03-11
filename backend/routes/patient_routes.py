from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.models import db, User, Doctor, Patient, Appointment, DoctorAvailability, Department, Treatment
from datetime import datetime, date

def is_patient():
    claims = get_jwt()
    return claims['role'] == 'Patient'

class SearchDoctors(Resource):
    @jwt_required()
    def get(self):
        """Search Doctors"""
        query = request.args.get('q', '').lower()
        dept_filter = request.args.get('dept', '').lower()
        
        doctors = Doctor.query.join(User).join(Department).all()
        
        results = []
        for d in doctors:
            if query and query not in d.user.full_name.lower():
                continue
            if dept_filter and dept_filter != d.department.department_name.lower():
                continue
                
            results.append({
                'id': d.id,
                'name': d.user.full_name,
                'department': d.department.department_name,
                'medical_id': d.medical_id
            })
        return results, 200

class GetDoctorAvailability(Resource):
    @jwt_required()
    def get(self, doctor_id):
        today = date.today()
        slots = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor_id,
            DoctorAvailability.date >= today,
            DoctorAvailability.is_active == True
        ).all()
        
        booked_appts = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.date >= today,
            Appointment.status != 'Cancelled'
        ).all()
        
        booked_keys = set((a.date, a.start_time) for a in booked_appts)
        
        available = []
        for s in slots:
            if (s.date, s.start_time) not in booked_keys:
                available.append({
                    'date': str(s.date),
                    'start_time': str(s.start_time),
                    'end_time': str(s.end_time)
                })
        
        available.sort(key=lambda x: (x['date'], x['start_time']))
        return available, 200

class BookAppointment(Resource):
    @jwt_required()
    def post(self):
        if not is_patient(): return {'message': 'Unauthorized'}, 403
        
        data = request.get_json()
        user = User.query.get(get_jwt_identity())
        patient = user.patient_profile
        
        doctor_id = data.get('doctor_id')
        date_str = data.get('date')
        time_str = data.get('start_time')
        
        appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        try:
            start_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            start_time = datetime.strptime(time_str, '%H:%M:%S').time()
        
        slot = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, date=appt_date, start_time=start_time
        ).first()
        
        if not slot:
            return {'message': 'Invalid or non-existent slot'}, 400
            
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id, date=appt_date, start_time=start_time
        ).filter(Appointment.status != 'Cancelled').first()
        
        if existing:
            return {'message': 'Slot already booked'}, 409
            
        new_appt = Appointment(
            doctor_id=doctor_id,
            patient_id=patient.id,
            date=appt_date,
            start_time=start_time,
            end_time=slot.end_time,
            status='Booked'
        )
        
        db.session.add(new_appt)
        db.session.commit()
        return {'message': 'Appointment Booked Successfully'}, 201

class PatientAppointments(Resource):
    @jwt_required()
    def get(self):
        if not is_patient(): return {'message': 'Unauthorized'}, 403
        user = User.query.get(get_jwt_identity())
        
        appts = Appointment.query.filter_by(patient_id=user.patient_profile.id).order_by(Appointment.date.desc()).all()
        
        result = []
        for a in appts:
            treatment = Treatment.query.filter_by(appointment_id=a.id).first()
            result.append({
                'id': a.id,
                'doctor_name': a.doctor.user.full_name,
                'department': a.doctor.department.department_name,
                'date': str(a.date),
                'start_time': str(a.start_time),
                'status': a.status,
                'diagnosis': treatment.diagnosis if treatment else None,
                'prescription': treatment.prescription if treatment else None,
                'notes': treatment.notes if treatment else None
            })
        return result, 200

class CancelAppointment(Resource):
    @jwt_required()
    def put(self, appointment_id):
        if not is_patient(): return {'message': 'Unauthorized'}, 403
        appt = Appointment.query.get_or_404(appointment_id)
        if appt.status == 'Completed': return {'message': 'Cannot cancel completed appointments'}, 400
        appt.status = 'Cancelled'
        db.session.commit()
        return {'message': 'Appointment Cancelled'}, 200

class PatientProfile(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        return {
            'full_name': user.full_name,
            'email': user.email,
            'mobile_no': user.mobile_no,
            'age': user.patient_profile.age,
            'gender': user.patient_profile.gender
        }, 200

    @jwt_required()
    def put(self):
        user = User.query.get(get_jwt_identity())
        data = request.get_json()
        if 'full_name' in data: user.full_name = data['full_name']
        if 'mobile_no' in data: user.mobile_no = data['mobile_no']
        if 'age' in data: user.patient_profile.age = data['age']
        db.session.commit()
        return {'message': 'Profile Updated'}, 200

class ExportCSV(Resource):
    @jwt_required()
    def get(self):
        if not is_patient(): return {'message': 'Unauthorized'}, 403
        user = User.query.get(get_jwt_identity())
        from celery_app import export_csv
        export_csv.delay(user.patient_profile.id, user.email)
        return {'message': 'Export started! You will receive an email with the download link.'}, 200