from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.models import db , User , Role
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = "secret_key"
    jwt = JWTManager(app)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
    app.config['SECRET_KEY'] = 'phull_sequrity'

    db.init_app(app)
    
    from routes.routes import api, cache
    from routes.Department_route import api, create_initial_departments

    api.init_app(app)

    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    cache.init_app(app)

    with app.app_context():
        db.create_all()
        create_initial_data()
        create_initial_departments()

    return app

def create_initial_data():
    
    if not Role.query.filter_by(name='Admin').first():
        db.session.add(Role(name='Admin'))
    if not Role.query.filter_by(name='Doctor').first():
        db.session.add(Role(name='Doctor'))
    if not Role.query.filter_by(name='Patient').first():
        db.session.add(Role(name='Patient'))
    db.session.commit()

    if not User.query.filter_by(email='admin@admin.com').first():
        admin_role= Role.query.filter_by(name='Admin').first()
        if admin_role:
            admin_user = User(full_name='Admin User',
                              email='admin@admin.com',
                              password_hash='admin@123',
                              mobile_no='9999999999',
                              flag='ADMIN',
                              role=[admin_role] )
            db.session.add(admin_user)
            db.session.commit()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
