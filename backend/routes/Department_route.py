from flask_restful import Api, Resource
from flask import request

from models.models import db, Department
from .routes import api

class Department_routes(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return{'message' : 'Enter the Data'} , 400
        if not data['department_name']:
            return{'message' : 'Enter the Department Name'} , 400
        if not data['description']:
            return{'message' : 'Enter Department Description'} , 400
        
        new_department = Department( department_name=data['department_name'], description=data['description'] )
        db.session.add(new_department)
        db.session.commit()
        return{"message": "New Department Added"}
    
    # def put(self, department_id=None):
        # data = request.get_json()

api.add_resource(Department_routes, '/add_department')

def create_initial_departments():

# department_name='', description= { "description" : "",
#                                   "issues_covered":[] }

    if not Department.query.filter_by(department_name='Cardiology').first():
        cardiology_dpt= Department(department_name='Cardiology', 
                               description= {
                                   "description":"The Cardiology Department specializes in the diagnosis and treatment of heart and vascular conditions. It includes non-invasive and invasive procedures to manage cardiovascular diseases.",
                                   "issues_covered": ["Coronary artery disease", "Heart failure", "Arrhythmias" , "Hypertension", "Valve disorders"]
                               })
        db.session.add(cardiology_dpt)

    if not Department.query.filter_by(department_name='Neurology').first():
        neurology_dpt = Department(department_name='Neurology', 
                               description= {
                                   "description":"The Neurology department deals with disorders of the brain, spinal cord, and nervous system. It offers both diagnostic and therapeutic services for a variety of neurological conditions.",
                                   "issues_covered":["Stroke", "Epilepsy", "Multiple sclerosis", "Parkinson's disease", "Migraines"]
                               })
        db.session.add(neurology_dpt)
    db.session.commit()