from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.models import db, User, Doctor, Appointment, Treatment, DoctorAvailability, Patient
from datetime import datetime, date, timedelta

def is_doctor():
    claims = get_jwt()
    return claims['role'] == 'Doctor'

class DoctorDashboard(Resource):
    @jwt_required()
    def get(self):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        doctor = user.doctor_profile
        if not doctor: return {'message': 'Doctor profile not found'}, 404

        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status != 'Cancelled'
        ).order_by(Appointment.date, Appointment.start_time).all()

        apt_data = []
        for apt in appointments:
            apt_data.append({
                'id': apt.id,
                'patient_name': apt.patient.user.full_name,
                'patient_id': apt.patient_id,
                'date': str(apt.date),
                'start_time': str(apt.start_time),
                'status': apt.status
            })
            
        return {
            'doctor_name': user.full_name,
            'appointments': apt_data,
            'total_patients': len(set(a.patient_id for a in appointments))
        }, 200

class ManageAvailability(Resource):
    @jwt_required()
    def get(self):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        user = User.query.get(get_jwt_identity())
        slots = user.doctor_profile.availability_slots
        sorted_slots = sorted(slots, key=lambda x: (x.date, x.start_time))
        
        return [{
            'id': s.id,
            'date': str(s.date),
            'day': s.date.strftime('%A'),
            'start_time': str(s.start_time),
            'end_time': str(s.end_time),
            'is_active': s.is_active
        } for s in sorted_slots], 200

    @jwt_required()
    def post(self):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        user = User.query.get(get_jwt_identity())
        doctor_id = user.doctor_profile.id
        
        target_days = data.get('days')
        start_str = data.get('start_time')
        end_str = data.get('end_time')
        
        if not target_days or not start_str or not end_str:
            return {'message': 'Missing fields'}, 400

        days_map = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, 
            "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
        }
        target_weekdays = [days_map[d] for d in target_days if d in days_map]

        today = date.today()
        generated_count = 0
        SLOT_DURATION = 30 
        
        try:
            start_t = datetime.strptime(start_str, '%H:%M')
            end_t = datetime.strptime(end_str, '%H:%M')

            for i in range(30):
                current_date = today + timedelta(days=i)
                if current_date.weekday() in target_weekdays:
                    slot_start = start_t
                    while slot_start + timedelta(minutes=SLOT_DURATION) <= end_t:
                        slot_end = slot_start + timedelta(minutes=SLOT_DURATION)
                        s_time = slot_start.time()
                        e_time = slot_end.time()
                        
                        exists = DoctorAvailability.query.filter_by(
                            doctor_id=doctor_id, date=current_date, start_time=s_time
                        ).first()
                        if not exists:
                            new_slot = DoctorAvailability(
                                doctor_id=doctor_id, date=current_date,
                                start_time=s_time, end_time=e_time
                            )
                            db.session.add(new_slot)
                            generated_count += 1
                        slot_start = slot_end
            
            db.session.commit()
            return {'message': f'Generated {generated_count} slots successfully'}, 201
        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 400

    @jwt_required()
    def delete(self, slot_id):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        slot = DoctorAvailability.query.get_or_404(slot_id)
        db.session.delete(slot)
        db.session.commit()
        return {'message': 'Slot removed'}, 200

class ManageAppointment(Resource):
    @jwt_required()
    def put(self, appointment_id):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        apt = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        if 'status' in data and data['status'] in ['Cancelled', 'Booked']:
            apt.status = data['status']
            db.session.commit()
            return {'message': 'Status updated'}, 200
        return {'message': 'Invalid status'}, 400

class AddTreatment(Resource):
    @jwt_required()
    def post(self, appointment_id):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        apt = Appointment.query.get_or_404(appointment_id)
        treatment = Treatment(appointment_id=apt.id, diagnosis=data['diagnosis'], prescription=data['prescription'], notes=data['notes'])
        apt.status = 'Completed'
        db.session.add(treatment)
        db.session.commit()
        return {'message': 'Treatment added & Appointment Completed'}, 201

class PatientHistory(Resource):
    @jwt_required()
    def get(self, patient_id):
        if not is_doctor(): return {'message': 'Unauthorized'}, 403
        treatments = Treatment.query.join(Appointment).filter(Appointment.patient_id == patient_id, Appointment.status == 'Completed').all()
        history = []
        for t in treatments:
            history.append({
                'date': str(t.appointment.date),
                'doctor': t.appointment.doctor.user.full_name,
                'diagnosis': t.diagnosis,
                'prescription': t.prescription,
                'notes': t.notes
            })
        return history, 200
