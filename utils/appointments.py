import json
import os

APPOINTMENTS_FILE = 'appointments.json'

def load_appointments():
    if not os.path.exists(APPOINTMENTS_FILE):
        return []
    with open(APPOINTMENTS_FILE, 'r') as f:
        return json.load(f)

def save_appointments(data):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def book_appointment(patient, doctor, date, time):
    appointments = load_appointments()
    new_appt = {
        "patient": patient,
        "doctor": doctor,
        "date": date,
        "time": time
    }
    appointments.append(new_appt)
    save_appointments(appointments)

def get_user_appointments(username):
    appointments = load_appointments()
    return [a for a in appointments if a['patient'] == username]

def get_doctor_appointments(doctor_name):
    appointments = load_appointments()
    return [a for a in appointments if a['doctor'] == doctor_name]
