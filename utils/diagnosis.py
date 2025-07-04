import boto3
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get AWS region and table name from .env
region = os.getenv('AWS_REGION_NAME', 'us-east-1')
diagnosis_table_name = os.getenv('DIAGNOSES_TABLE_NAME', 'Diagnoses')

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=region)
diagnosis_table = dynamodb.Table(diagnosis_table_name)

# ✅ Submit a diagnosis (Doctor adds diagnosis for patient)
def submit_diagnosis(patient, doctor, notes):
    diagnosis_id = str(uuid.uuid4())
    diagnosis_table.put_item(Item={
        'diagnosis_id': diagnosis_id,
        'patient': patient,
        'doctor': doctor,
        'notes': notes
    })

# ✅ View diagnoses by doctor
def get_doctor_diagnoses(doctor):
    response = diagnosis_table.scan()
    items = response.get('Items', [])
    return [d for d in items if d['doctor'] == doctor]

# ✅ View diagnoses by patient
def get_patient_diagnoses(patient):
    response = diagnosis_table.scan()
    items = response.get('Items', [])
    return [d for d in items if d['patient'] == patient]