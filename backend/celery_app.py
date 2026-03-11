from celery import Celery

celeryApp = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)
celeryApp.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

from mail import send_mail
from flask import Flask
from models.models import db, User, Doctor, Patient, Appointment, Treatment

def make_celery_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
    db.init_app(app)
    return app

@celeryApp.task()
def daily_reminder():
    app = make_celery_app()
    with app.app_context():
        from datetime import date
        today = date.today()
        todays_appointments = Appointment.query.filter_by(date=today, status='Booked').all()
        count = 0
        for apt in todays_appointments:
            patient_user = apt.patient.user
            doctor_user = apt.doctor.user
            to = patient_user.email
            subject = "Appointment Reminder - HMS"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background:#f6f9fc; margin:0; padding:20px;">
                <div style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
                <div style="background:#4a90e2; color:#ffffff; padding:20px 24px;">
                    <h1 style="margin:0; font-size:20px;">Appointment Reminder</h1>
                </div>
                <div style="padding:24px; color:#333333; line-height:1.6; font-size:15px;">
                    <p>Hello <strong>{patient_user.full_name}</strong>,</p>
                    <p>This is a reminder that you have an appointment scheduled today.</p>
                    <table style="width:100%; border-collapse:collapse; margin:16px 0;">
                        <tr><td style="padding:8px; border:1px solid #eee; font-weight:bold;">Doctor</td><td style="padding:8px; border:1px solid #eee;">Dr. {doctor_user.full_name}</td></tr>
                        <tr><td style="padding:8px; border:1px solid #eee; font-weight:bold;">Date</td><td style="padding:8px; border:1px solid #eee;">{apt.date}</td></tr>
                        <tr><td style="padding:8px; border:1px solid #eee; font-weight:bold;">Time</td><td style="padding:8px; border:1px solid #eee;">{apt.start_time}</td></tr>
                    </table>
                    <p>Please arrive 10 minutes before your scheduled time.</p>
                </div>
                <div style="background:#f2f6fb; color:#6b7280; padding:12px 24px; font-size:13px;">
                    Hospital Management System
                </div>
                </div>
            </body>
            </html>
            """
            send_mail(to, subject, body)
            count += 1
    return f"Daily reminders sent to {count} patients"

@celeryApp.task()
def monthly_reminder():
    app = make_celery_app()
    with app.app_context():
        from datetime import date, timedelta
        today = date.today()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        doctors = Doctor.query.all()
        count = 0
        for doctor in doctors:
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.date >= last_month_start,
                Appointment.date <= last_month_end
            ).all()

            if not appointments:
                continue

            completed = [a for a in appointments if a.status == 'Completed']
            cancelled = [a for a in appointments if a.status == 'Cancelled']

            rows = ""
            for apt in appointments:
                treatment = Treatment.query.filter_by(appointment_id=apt.id).first()
                diagnosis = ""
                prescription = ""
                if treatment:
                    diagnosis = treatment.diagnosis.get('text', '') if isinstance(treatment.diagnosis, dict) else str(treatment.diagnosis)
                    prescription = ', '.join(treatment.prescription.get('list', [])) if isinstance(treatment.prescription, dict) else str(treatment.prescription)
                rows += f"""
                <tr>
                    <td style="padding:8px; border:1px solid #ddd;">{apt.date}</td>
                    <td style="padding:8px; border:1px solid #ddd;">{apt.patient.user.full_name}</td>
                    <td style="padding:8px; border:1px solid #ddd;">{apt.status}</td>
                    <td style="padding:8px; border:1px solid #ddd;">{diagnosis}</td>
                    <td style="padding:8px; border:1px solid #ddd;">{prescription}</td>
                </tr>
                """

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background:#f6f9fc; margin:0; padding:20px;">
                <div style="max-width:700px; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
                <div style="background:#2c3e50; color:#ffffff; padding:20px 24px;">
                    <h1 style="margin:0; font-size:20px;">Monthly Activity Report</h1>
                    <p style="margin:4px 0 0; font-size:14px; opacity:0.9;">{last_month_start.strftime('%B %Y')}</p>
                </div>
                <div style="padding:24px; color:#333333; line-height:1.6; font-size:15px;">
                    <p>Dear <strong>Dr. {doctor.user.full_name}</strong>,</p>
                    <p>Here is your activity summary for {last_month_start.strftime('%B %Y')}:</p>
                    <div style="display:flex; gap:12px; margin:16px 0;">
                        <div style="background:#e8f5e9; padding:12px 20px; border-radius:6px; text-align:center; flex:1;">
                            <div style="font-size:24px; font-weight:bold; color:#2e7d32;">{len(appointments)}</div>
                            <div style="font-size:13px; color:#555;">Total</div>
                        </div>
                        <div style="background:#e3f2fd; padding:12px 20px; border-radius:6px; text-align:center; flex:1;">
                            <div style="font-size:24px; font-weight:bold; color:#1565c0;">{len(completed)}</div>
                            <div style="font-size:13px; color:#555;">Completed</div>
                        </div>
                        <div style="background:#fce4ec; padding:12px 20px; border-radius:6px; text-align:center; flex:1;">
                            <div style="font-size:24px; font-weight:bold; color:#c62828;">{len(cancelled)}</div>
                            <div style="font-size:13px; color:#555;">Cancelled</div>
                        </div>
                    </div>
                    <h3 style="margin-top:20px;">Appointment Details</h3>
                    <table style="width:100%; border-collapse:collapse;">
                        <thead>
                            <tr style="background:#f5f5f5;">
                                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Date</th>
                                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Patient</th>
                                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Status</th>
                                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Diagnosis</th>
                                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Prescription</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
                <div style="background:#f2f6fb; color:#6b7280; padding:12px 24px; font-size:13px;">
                    Hospital Management System - Auto-generated Report
                </div>
                </div>
            </body>
            </html>
            """
            send_mail(doctor.user.email, f"Monthly Report - {last_month_start.strftime('%B %Y')}", body)
            count += 1
    return f"Monthly reports sent to {count} doctors"

@celeryApp.task()
def export_csv(patient_id, email):
    import csv
    import os
    app = make_celery_app()
    with app.app_context():
        appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.date.desc()).all()
        patient = Patient.query.get(patient_id)

        os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)
        filepath = os.path.join(app.root_path, 'static', f'export_{patient_id}.csv')

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Patient ID', 'Patient Name', 'Doctor', 'Department', 'Date', 'Time', 'Status', 'Diagnosis', 'Prescription', 'Notes'])
            for apt in appointments:
                treatment = Treatment.query.filter_by(appointment_id=apt.id).first()
                diagnosis = ''
                prescription = ''
                notes = ''
                if treatment:
                    diagnosis = treatment.diagnosis.get('text', '') if isinstance(treatment.diagnosis, dict) else str(treatment.diagnosis)
                    prescription = ', '.join(treatment.prescription.get('list', [])) if isinstance(treatment.prescription, dict) else str(treatment.prescription)
                    notes = treatment.notes
                writer.writerow([
                    patient_id,
                    patient.user.full_name,
                    apt.doctor.user.full_name,
                    apt.doctor.department.department_name,
                    str(apt.date),
                    str(apt.start_time),
                    apt.status,
                    diagnosis,
                    prescription,
                    notes
                ])

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f6f9fc; margin:0; padding:20px;">
            <div style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            <div style="background:#27ae60; color:#ffffff; padding:20px 24px;">
                <h1 style="margin:0; font-size:20px;">CSV Export Ready</h1>
            </div>
            <div style="padding:24px; color:#333333; line-height:1.6; font-size:15px;">
                <p>Hello <strong>{patient.user.full_name}</strong>,</p>
                <p>Your treatment history CSV export is ready for download.</p>
                <div style="text-align:center; margin:20px 0;">
                    <a href="http://127.0.0.1:5000/static/export_{patient_id}.csv" style="display:inline-block; background:#27ae60; color:#ffffff; text-decoration:none; padding:10px 24px; border-radius:6px; font-weight:600;">Download CSV</a>
                </div>
            </div>
            <div style="background:#f2f6fb; color:#6b7280; padding:12px 24px; font-size:13px;">
                Hospital Management System
            </div>
            </div>
        </body>
        </html>
        """
        send_mail(email, "Treatment History Export Ready", body)
    return f"CSV exported for patient {patient_id}"

from celery.schedules import crontab

celeryApp.conf.beat_schedule = {
    'daily_reminders': {
        'task': 'celery_app.daily_reminder',
        'schedule': crontab(hour=8, minute=0)
    },
    'montly_reminders': {
        'task': 'celery_app.monthly_reminder',
        'schedule': crontab(day_of_month=2, hour=16, minute=30)
    }
}
