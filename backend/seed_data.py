from app import create_app
from models.models import db, User, Role, Doctor, Patient, Appointment, Treatment, DoctorAvailability, Department
from datetime import date, time, timedelta
import random

app = create_app()

with app.app_context():
    doctor_role = Role.query.filter_by(name='Doctor').first()
    patient_role = Role.query.filter_by(name='Patient').first()
    departments = Department.query.all()

    doctors_data = [
        {"name": "Dr. Arjun Mehta", "email": "doctor@1", "mobile": "9000000001", "medical_id": "MED001", "dept_idx": 0},
        {"name": "Dr. Priya Sharma", "email": "doctor@2", "mobile": "9000000002", "medical_id": "MED002", "dept_idx": 1},
        {"name": "Dr. Rahul Verma", "email": "doctor@3", "mobile": "9000000003", "medical_id": "MED003", "dept_idx": 2},
        {"name": "Dr. Sneha Gupta", "email": "doctor@4", "mobile": "9000000004", "medical_id": "MED004", "dept_idx": 3},
        {"name": "Dr. Vikram Singh", "email": "doctor@5", "mobile": "9000000005", "medical_id": "MED005", "dept_idx": 0},
    ]

    patients_data = [
        {"name": "Amit Kumar", "email": "patient@1", "mobile": "8000000001", "age": 28, "gender": "Male"},
        {"name": "Neha Patel", "email": "patient@2", "mobile": "8000000002", "age": 35, "gender": "Female"},
        {"name": "Ravi Joshi", "email": "patient@3", "mobile": "8000000003", "age": 45, "gender": "Male"},
        {"name": "Sunita Devi", "email": "patient@4", "mobile": "8000000004", "age": 52, "gender": "Female"},
        {"name": "Karan Malhotra", "email": "patient@5", "mobile": "8000000005", "age": 30, "gender": "Male"},
        {"name": "Pooja Reddy", "email": "patient@6", "mobile": "8000000006", "age": 22, "gender": "Female"},
        {"name": "Deepak Yadav", "email": "patient@7", "mobile": "8000000007", "age": 60, "gender": "Male"},
        {"name": "Ananya Iyer", "email": "patient@8", "mobile": "8000000008", "age": 27, "gender": "Female"},
    ]

    created_doctors = []
    for d in doctors_data:
        if User.query.filter_by(email=d["email"]).first():
            print(f"Skipping {d['email']} (already exists)")
            existing_doc = Doctor.query.join(User).filter(User.email == d["email"]).first()
            if existing_doc:
                created_doctors.append(existing_doc)
            continue
        user = User(full_name=d["name"], email=d["email"], mobile_no=d["mobile"])
        user.set_password("pass")
        user.roles.append(doctor_role)
        doctor = Doctor(medical_id=d["medical_id"], department_id=departments[d["dept_idx"]].id)
        user.doctor_profile = doctor
        db.session.add(user)
        db.session.add(doctor)
        db.session.flush()
        created_doctors.append(doctor)
        print(f"Created doctor: {d['email']} / pass")

    created_patients = []
    for p in patients_data:
        if User.query.filter_by(email=p["email"]).first():
            print(f"Skipping {p['email']} (already exists)")
            existing_pat = Patient.query.join(User).filter(User.email == p["email"]).first()
            if existing_pat:
                created_patients.append(existing_pat)
            continue
        user = User(full_name=p["name"], email=p["email"], mobile_no=p["mobile"])
        user.set_password("pass")
        user.roles.append(patient_role)
        patient = Patient(age=p["age"], gender=p["gender"])
        user.patient_profile = patient
        db.session.add(user)
        db.session.add(patient)
        db.session.flush()
        created_patients.append(patient)
        print(f"Created patient: {p['email']} / pass")

    db.session.commit()

    for doc in created_doctors:
        today = date.today()
        for i in range(14):
            d = today + timedelta(days=i)
            if d.weekday() < 6:
                exists = DoctorAvailability.query.filter_by(doctor_id=doc.id, date=d, start_time=time(9, 0)).first()
                if not exists:
                    db.session.add(DoctorAvailability(doctor_id=doc.id, date=d, start_time=time(9, 0), end_time=time(10, 0)))
                    db.session.add(DoctorAvailability(doctor_id=doc.id, date=d, start_time=time(10, 0), end_time=time(11, 0)))
                    db.session.add(DoctorAvailability(doctor_id=doc.id, date=d, start_time=time(11, 0), end_time=time(12, 0)))
                    db.session.add(DoctorAvailability(doctor_id=doc.id, date=d, start_time=time(14, 0), end_time=time(15, 0)))
                    db.session.add(DoctorAvailability(doctor_id=doc.id, date=d, start_time=time(15, 0), end_time=time(16, 0)))
    db.session.commit()
    print("Availability slots created")

    diagnoses = [
        {"text": "Viral Fever"},
        {"text": "Migraine"},
        {"text": "Lower Back Pain"},
        {"text": "Hypertension Stage 1"},
        {"text": "Common Cold with Throat Infection"},
        {"text": "Type 2 Diabetes - Early Stage"},
        {"text": "Knee Ligament Strain"},
        {"text": "Cardiac Arrhythmia"},
        {"text": "Gastritis"},
        {"text": "Vitamin D Deficiency"},
    ]

    prescriptions = [
        {"list": ["Paracetamol 500mg (Morning/Night)", "Rest for 3 days"]},
        {"list": ["Sumatriptan 50mg (As needed)", "Avoid screen time"]},
        {"list": ["Ibuprofen 400mg (Twice daily)", "Hot compress", "Physiotherapy referral"]},
        {"list": ["Amlodipine 5mg (Once daily)", "Low sodium diet", "Daily walking 30 min"]},
        {"list": ["Azithromycin 500mg (3 days)", "Warm salt water gargle", "Vitamin C tablets"]},
        {"list": ["Metformin 500mg (Morning)", "Low sugar diet", "HbA1c test in 3 months"]},
        {"list": ["Diclofenac gel (Apply twice)", "Knee brace recommended", "Avoid stairs"]},
        {"list": ["Bisoprolol 2.5mg (Once daily)", "ECG follow-up in 2 weeks"]},
        {"list": ["Pantoprazole 40mg (Before breakfast)", "Avoid spicy food"]},
        {"list": ["Cholecalciferol 60000 IU (Weekly)", "Sunlight exposure 20 min daily"]},
    ]

    notes_list = [
        "Patient responded well. Follow up in 1 week.",
        "Condition stable. Monitor blood pressure daily.",
        "Recommend further tests if symptoms persist.",
        "Patient advised lifestyle changes. Review in 2 weeks.",
        "Improvement observed. Continue medications.",
        "Referred to specialist for further evaluation.",
        "Patient to return for blood work next week.",
        "Recovery on track. Reduce dosage gradually.",
        "No complications observed. Standard recovery expected.",
        "Chronic condition - long term management plan discussed.",
    ]

    today = date.today()
    appointment_count = 0

    for pat_idx, patient in enumerate(created_patients):
        num_past = random.randint(3, 6)
        for i in range(num_past):
            doc = created_doctors[random.randint(0, len(created_doctors) - 1)]
            past_date = today - timedelta(days=random.randint(5, 90))
            slot_time = random.choice([time(9, 0), time(10, 0), time(11, 0), time(14, 0), time(15, 0)])

            existing = Appointment.query.filter_by(
                doctor_id=doc.id, date=past_date, start_time=slot_time
            ).filter(Appointment.status != 'Cancelled').first()
            if existing:
                continue

            status = random.choice(["Completed", "Completed", "Completed", "Cancelled"])
            apt = Appointment(
                doctor_id=doc.id, patient_id=patient.id,
                date=past_date, start_time=slot_time,
                end_time=time(slot_time.hour + 1, 0),
                status=status
            )
            db.session.add(apt)
            db.session.flush()

            if status == "Completed":
                idx = random.randint(0, len(diagnoses) - 1)
                treatment = Treatment(
                    appointment_id=apt.id,
                    diagnosis=diagnoses[idx],
                    prescription=prescriptions[idx],
                    notes=notes_list[random.randint(0, len(notes_list) - 1)]
                )
                db.session.add(treatment)

            appointment_count += 1

    for pat_idx in range(min(5, len(created_patients))):
        patient = created_patients[pat_idx]
        doc = created_doctors[pat_idx % len(created_doctors)]
        future_date = today + timedelta(days=random.randint(1, 7))
        if future_date.weekday() >= 6:
            future_date += timedelta(days=1)
        slot_time = random.choice([time(9, 0), time(10, 0), time(14, 0)])

        existing = Appointment.query.filter_by(
            doctor_id=doc.id, date=future_date, start_time=slot_time
        ).filter(Appointment.status != 'Cancelled').first()
        if not existing:
            apt = Appointment(
                doctor_id=doc.id, patient_id=patient.id,
                date=future_date, start_time=slot_time,
                end_time=time(slot_time.hour + 1, 0),
                status="Booked"
            )
            db.session.add(apt)
            appointment_count += 1

    db.session.commit()
    print(f"Created {appointment_count} appointments with treatments")
    print("\n--- LOGIN CREDENTIALS ---")
    print("Admin:    admin@admin.com / admin@admin.com")
    for d in doctors_data:
        print(f"Doctor:   {d['email']} / pass")
    for p in patients_data:
        print(f"Patient:  {p['email']} / pass")
