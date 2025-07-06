from flask import Flask, render_template, request, redirect, session
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# 🔐 Load values from .env
SECRET_KEY = os.getenv('SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION_NAME','us-east-1')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'temp_secret_123!@#xyz987'

# ✅ Import DB logic from utils
from utils.aws_dynamo import register_user, validate_login, load_users
from utils.appointments import book_appointment, get_user_appointments, get_doctor_appointments
from utils.diagnosis import submit_diagnosis, get_doctor_diagnoses, get_patient_diagnoses

# --------- AWS SNS Configuration ---------
sns = boto3.client('sns', region_name=AWS_REGION)

def send_notification(message, subject='Notification from MedTrack'):
    if not SNS_TOPIC_ARN or "dummy" in SNS_TOPIC_ARN:
        print("📢 Skipping SNS notification (not configured)")
        return None
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        print("✅ SNS message sent:", response)
        return response
    except Exception as e:
        print("❌ Error sending SNS message:", e)
        return None

# ---------------- Routes ----------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        register_user(data['username'], data['password'], data['role'])
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = validate_login(username, password)
        if role:
            session['username'] = username
            session['role'] = role
            return redirect('/dashboard')
        return "Invalid Credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        doctor = request.form['doctor']
        date = request.form['date']
        time = request.form['time']
        book_appointment(session['username'], doctor, date, time)

        # 🔔 Send SNS notification
        message = f"Appointment booked by {session['username']} with Dr. {doctor} on {date} at {time}."
        send_notification(message, subject="New Appointment Booked")

        return redirect('/appointments')
    return render_template('book.html')

@app.route('/appointments')
def appointments_view():
    if 'username' not in session:
        return redirect('/')
    user_appointments = get_user_appointments(session['username'])
    return render_template('appointments.html', appointments=user_appointments)

@app.route('/doctor-appointments')
def doctor_appointments():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect('/')
    appts = get_doctor_appointments(session['username'])
    return render_template('doctor_appointments.html', appointments=appts)

@app.route('/submit-diagnosis', methods=['GET', 'POST'])
def submit_diagnosis_route():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect('/')
    
    if request.method == 'POST':
        patient = request.form['patient']
        notes = request.form['notes']
        submit_diagnosis(patient, session['username'], notes)

        # 🔔 SNS notification
        message = f"Dr. {session['username']} submitted a diagnosis for patient {patient}."
        send_notification(message, subject="New Diagnosis Submitted")

        return render_template("diagnosis_success.html")

    patients = [u['username'] for u in load_users() if u['role'] == 'patient']
    return render_template('submit_diagnosis.html', patients=patients)

@app.route('/view-diagnosis')
def view_diagnosis_route():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect('/')
    diagnoses = get_doctor_diagnoses(session['username'])
    return render_template('view_diagnosis.html', diagnoses=diagnoses) 

@app.route('/my-diagnosis')
def my_diagnosis():
    if 'username' not in session or session['role'] != 'patient':
        return redirect('/')
    diagnoses = get_patient_diagnoses(session['username'])
    return render_template('my_diagnosis.html', diagnoses=diagnoses)

# ------------ Run the App ------------
# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
