from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    flag = db.Column(db.String(10), nullable = False, default='active')

    role = db.relationship('Role', secondary='user_role')

class Doctor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department_id= db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    medical_id= db.Column(db.String(50), nullable=False, unique=True)
    availability = db.Column(db.JSON, nullable=False)

class Patient(db.Model):
    id =  db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    mobile_no = db.Column(db.String(10), unique=True, nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), unique =True , nullable = False)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable = False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable = False)
    diagnosis= db.Column(db.JSON, nullable = False)
    prescription = db.Column(db.JSON, nullable = False)
    notes= db.Column(db.String, nullable = False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String, nullable = True)
    description = db.Column(db.String, nullable=False)
