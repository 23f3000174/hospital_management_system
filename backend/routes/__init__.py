from flask import Blueprint
from flask_restful import Api

auth_bp = Blueprint( 'auth', __name__, url_prefix = '/api/auth')
admin_bp = Blueprint( 'admin', __name__, url_prefix = '/api/admin')
doctor_bp = Blueprint( 'doctor', __name__, url_prefix = '/api/doctor')
patient_bp = Blueprint( 'patient', __name__, url_prefix = '/api/patient')
public_bp = Blueprint( 'public', __name__, url_prefix = '/api/public')

auth_api = Api(auth_bp)
admin_api = Api(admin_bp)
doctor_api = Api(doctor_bp)
patient_api = Api(patient_bp)
public_api = Api(public_bp)


from .auth_routes import Register, Login

auth_api.add_resource(Login, '/login')
auth_api.add_resource(Register, '/register')
