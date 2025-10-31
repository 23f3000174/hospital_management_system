from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.models import db , User , Role

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
    app.config['SECRET_KEY'] = 'phull_sequrity'

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print('cid before')
        create_initial_data()
        print('cid after')

    @app.route('/')
    def index():
        return "Hello from flask"

    return app

def create_initial_data():

    print('create initial data called')
    
    if not Role.query.filter_by(name='admin').first():
        db.session.add(Role(name='admin'))
    print('admin added')

    if not Role.query.filter_by(name='doctor').first():
        db.session.add(Role(name='doctor'))
    print('Doctor added')

    if not Role.query.filter_by(name='patient').first():
        db.session.add(Role(name='patient'))
    print('Patient added')

    db.session.commit()

    if not User.query.filter_by(email='admin@admin.com').first():

        print('checked if admin is already created')

        admin_role= Role.query.filter_by(name='admin').first()
        print('created admin role  ', admin_role)
        if admin_role:
            admin_user = User(full_name='Admin User',
                              email='admin@admin.com',
                              password='admin@123',
                              flag='Papa',
                              role=[admin_role] )
            db.session.add(admin_user)
            db.session.commit()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
