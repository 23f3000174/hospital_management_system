from flask_restful import Resource
from models.models import Department

class DepartmentList(Resource):
    def get(self):
        depts = Department.query.all()
        return [
            {
                'id': d.id, 
                'name': d.department_name, 
                'description': d.description 
            } 
            for d in depts
        ], 200