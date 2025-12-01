from flask import Blueprint
from flask_restful import Api

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
doctor_bp = Blueprint('doctor', __name__, url_prefix='/api/doctor')
patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')
public_bp = Blueprint('public', __name__, url_prefix='/api/public')

auth_api = Api(auth_bp)
admin_api = Api(admin_bp)
doctor_api = Api(doctor_bp)
patient_api = Api(patient_bp)
public_api = Api(public_bp)

from .auth_routes import Register, Login
from .admin_routes import AdminDashboard, ManageDepartment, ManageDoctor, ManagePatient
from .public_routes import DepartmentList

auth_api.add_resource(Login, '/login')
auth_api.add_resource(Register, '/register')

admin_api.add_resource(AdminDashboard, '/dashboard')

admin_api.add_resource(ManageDoctor, '/doctor', '/doctor/<int:doctor_id>')
admin_api.add_resource(ManageDepartment, '/department', '/department/<int:department_id>')
admin_api.add_resource(ManagePatient, '/patient', '/patient/<int:patient_id>')

public_api.add_resource(DepartmentList, '/departments')

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