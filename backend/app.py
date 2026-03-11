from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from models.models import db, User, Role
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = "secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
    app.config['SECRET_KEY'] = 'phull_sequrity'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/2'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60

    CORS(app, resources={r"/*": {"origins": "*"}}, 
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    db.init_app(app)
    jwt = JWTManager(app)

    from routes import cache, create_initial_departments, auth_bp, admin_bp, public_bp, doctor_bp, patient_bp
    cache.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)

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
        admin_role = Role.query.filter_by(name='Admin').first()
        if admin_role:
            admin_user = User(
                full_name='Admin User',
                email='admin@admin.com',
                mobile_no='9999999999',
                flag='active'
            )
            admin_user.set_password('admin@admin.com')
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)