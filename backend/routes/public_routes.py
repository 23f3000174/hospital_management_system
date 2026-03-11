from flask_restful import Resource
from models.models import Department
from routes import cache

class DepartmentList(Resource):
    def get(self):
        cached = cache.get('department_list')
        if cached:
            return cached
        depts = Department.query.all()
        result = [
            {
                'id': d.id, 
                'name': d.department_name, 
                'description': d.description 
            } 
            for d in depts
        ]
        cache.set('department_list', result, timeout=60)
        return result, 200