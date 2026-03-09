from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
doctor_bp = Blueprint('doctor', __name__, url_prefix='/api/doctor')
patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')
public_bp = Blueprint('public', __name__, url_prefix='/api/public')

CORS(auth_bp)
CORS(admin_bp)
CORS(doctor_bp)
CORS(patient_bp)
CORS(public_bp)

auth_api = Api(auth_bp)
admin_api = Api(admin_bp)
doctor_api = Api(doctor_bp)
patient_api = Api(patient_bp)
public_api = Api(public_bp)

from .auth_routes import Register, Login
from .admin_routes import AdminDashboard, ManageDepartment, ManageDoctor, ManagePatient
from .public_routes import DepartmentList
from .doctor_routes import DoctorDashboard, ManageAvailability, ManageAppointment, AddTreatment, PatientHistory
from .patient_routes import SearchDoctors, GetDoctorAvailability, BookAppointment, PatientAppointments, CancelAppointment, PatientProfile

auth_api.add_resource(Login, '/login')
auth_api.add_resource(Register, '/register')

public_api.add_resource(DepartmentList, '/departments')

admin_api.add_resource(AdminDashboard, '/dashboard')
admin_api.add_resource(ManageDoctor, '/doctor', '/doctor/<int:doctor_id>')
admin_api.add_resource(ManageDepartment, '/department', '/department/<int:department_id>')
admin_api.add_resource(ManagePatient, '/patient', '/patient/<int:patient_id>')

doctor_api.add_resource(DoctorDashboard, '/dashboard')
doctor_api.add_resource(ManageAvailability, '/availability', '/availability/<int:slot_id>')
doctor_api.add_resource(ManageAppointment, '/appointment/<int:appointment_id>')
doctor_api.add_resource(AddTreatment, '/treatment/<int:appointment_id>')
doctor_api.add_resource(PatientHistory, '/patient-history/<int:patient_id>')

patient_api.add_resource(SearchDoctors, '/search')
patient_api.add_resource(GetDoctorAvailability, '/availability/<int:doctor_id>')
patient_api.add_resource(BookAppointment, '/book')
patient_api.add_resource(PatientAppointments, '/my-appointments')
patient_api.add_resource(CancelAppointment, '/appointment/<int:appointment_id>/cancel')
patient_api.add_resource(PatientProfile, '/profile')

from models.models import db, Department
def create_initial_departments():
    departments_data = [
        {
            "name": "Cardiology",
            "desc": "The Cardiology Department specializes in the diagnosis and treatment of heart and vascular conditions.",
            "issues": ["Coronary artery disease", "Heart failure", "Arrhythmias", "Hypertension"]
        },
        {
            "name": "Neurology",
            "desc": "The Neurology Department deals with disorders of the nervous system.",
            "issues": ["Stroke", "Epilepsy", "Migraines", "Parkinson's disease"]
        },
        {
            "name": "Orthopedics",
            "desc": "The Orthopedics Department focuses on the musculoskeletal system.",
            "issues": ["Fractures", "Arthritis", "Ligament tears", "Back pain"]
        },
        {
            "name": "General Medicine",
            "desc": "General Medicine deals with the prevention, diagnosis, and non-surgical treatment of adult diseases.",
            "issues": ["Fever", "Flu", "Diabetes management", "Infections"]
        }
    ]
    for d in departments_data:
        if not Department.query.filter_by(department_name=d['name']).first():
            new_dept = Department(
                department_name=d['name'],
                description={"description": d['desc'], "issues_covered": d['issues']}
            )
            db.session.add(new_dept)
    db.session.commit()