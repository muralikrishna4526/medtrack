import json
import os

DIAGNOSIS_FILE = 'diagnoses.json'

# Load diagnosis data from JSON file
def load_diagnoses():
    if os.path.exists(DIAGNOSIS_FILE):
        with open(DIAGNOSIS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save diagnosis data to JSON file
def save_diagnoses(data):
    with open(DIAGNOSIS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Called by patients to submit diagnosis info
def submit_diagnosis(patient, doctor, notes):
    diagnoses = load_diagnoses()
    new_entry = {
        "patient": patient,
        "doctor": doctor,
        "notes": notes
    }
    diagnoses.append(new_entry)
    save_diagnoses(diagnoses)

# Called by doctors to view their patient's reports
def get_doctor_diagnoses(doctor):
    diagnoses = load_diagnoses()
    return [d for d in diagnoses if d['doctor'] == doctor]
