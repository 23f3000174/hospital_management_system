from flask_sqlalchemy import SQLAlchemy

import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(128), nullable = False)
    mobile_no = db.Column(db.String(10), nullable=False)
    flag = db.Column(db.String(10), nullable = False, default='active')

    roles = db.relationship('Role', secondary='user_role', back_populate='users')
    doctor_profile = db.relationship('Doctor', back_populates='user', uselist=False)
    patient_profile = db.relationship('Patient', back_populates='user', uselist=False)

    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        self.password_hash = hashed.decode('utf-8') 
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        stored_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)
    
class Doctor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department_id= db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    medical_id= db.Column(db.String(50), nullable=False, unique=True)
    
    user = db.relationship('User', back_populates='doctor_profile')
    department = db.relationship('Department', back_populates='doctors')
    
    availability_slots = db.relationship( 'DoctorAvailability', back_populates='doctor', cascade='all, delete-orphan', order_by='(DoctorAvailability.date, DoctorAvailability.start_time)')

class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'), nullable=False, index=True)

    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Patient(db.Model):
    id =  db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable = False)

    user = db.relationship('User', back_populates='patient_profile')
    appointments = db.relationship('Appointment', back_populates='patient')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), unique =True , nullable = False)

    users = db.relationship('User', secondary='user_role', back_populates='roles')

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    status = db.Column(db.String, nullable = False)

    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')
    
    treatment = db.relationship('Treatment', back_populates='appointment', uselist=False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable = False)
    diagnosis= db.Column(db.JSON, nullable = False)
    prescription = db.Column(db.JSON, nullable = False)
    notes= db.Column(db.String, nullable = False)

    appointment = db.relationship('Appointment', back_populates='treatment')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String, nullable = True)
    description = db.Column(db.JSON, nullable=False)

    doctors = db.relationship('Doctor', back_populates='department')
