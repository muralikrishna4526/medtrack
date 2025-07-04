import boto3
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get region and table name from .env
region = os.getenv('AWS_REGION_NAME', 'us-east-1')
appointments_table_name = os.getenv('APPOINTMENTS_TABLE_NAME', 'Appointments')

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=region)
appointments_table = dynamodb.Table(appointments_table_name)

# ✅ Book an appointment
def book_appointment(patient, doctor, date, time):
    appointment_id = str(uuid.uuid4())
    appointments_table.put_item(Item={
        'appointment_id': appointment_id,
        'patient': patient,
        'doctor': doctor,
        'date': date,
        'time': time
    })

# ✅ Get appointments for a specific patient
def get_user_appointments(username):
    response = appointments_table.scan()
    items = response.get('Items', [])
    return [a for a in items if a['patient'] == username]

# ✅ Get appointments for a specific doctor
def get_doctor_appointments(doctor_name):
    response = appointments_table.scan()
    items = response.get('Items', [])
    return [a for a in items if a['doctor'] == doctor_name]