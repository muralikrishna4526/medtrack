from utils.appointments import book_appointment, get_user_appointments, get_doctor_appointments
from flask import Flask, render_template, request, redirect, session
from utils.aws_dynamo import register_user, validate_login
from utils.diagnosis import submit_diagnosis, get_doctor_diagnoses
from utils.diagnosis import get_patient_diagnoses


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a stronger key in production

# ---------------- Home Page ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        register_user(data['username'], data['password'], data['role'])
        return redirect('/login')
    return render_template('register.html')

# ---------------- Login (GET) ----------------
@app.route('/login')
def show_login():
    return render_template('login.html')

# ---------------- Login (POST) ----------------
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    role = validate_login(username, password)
    if role:
        session['username'] = username
        session['role'] = role
        return redirect('/dashboard')
    return "Invalid Credentials"

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- Dashboard ----------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'], role=session['role'])

# ---------------- Book Appointment ----------------
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        doctor = request.form['doctor']
        date = request.form['date']
        time = request.form['time']
        book_appointment(session['username'], doctor, date, time)
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
        return render_template("diagnosis_success.html")

    from utils.auth import load_users
    users = load_users()
    patients = [u['username'] for u in users if u['role'] == 'patient']

    return render_template('submit_diagnosis.html', patients=patients)


# ---------------- View Diagnosis ----------------
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





# ---------------- Run the App ----------------
if __name__ == '__main__':
    app.run(debug=True)
