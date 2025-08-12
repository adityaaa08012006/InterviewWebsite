# Anantya 2025 Website - Flask Backend
# ACM PCCoE Student Chapter's Flagship Technical Event

import os
import csv
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'anantya_2025_secret_key_acm_pccoe'  # Change this in production

# Configuration
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(DATA_DIR, 'registrations.csv')

REQUIRED_FIELDS = ['fullname', 'email', 'phone', 'department', 'year']

# Consistent headers (no spaces so DictReader is safe)
HEADERS = [
    'RegistrationID', 'FullName', 'Email', 'Phone',
    'Department', 'Year', 'College', 'RegDate', 'RegTime'
]

# Initialize CSV file with headers if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        print("CSV file initialized with headers")

# Utility Functions
def validate_email(email):
    """Validate email format"""
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    return re.match(r'^\d{10}$', phone) is not None

def email_exists(email):
    """Check if email already exists in registrations"""
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('Email', '').lower() == email.lower():
                    return True
        return False
    except FileNotFoundError:
        return False

def phone_exists(phone):
    """Check if phone number already exists in registrations"""
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('Phone', '') == phone:
                    return True
        return False
    except FileNotFoundError:
        return False

def generate_registration_id():
    """Generate unique registration ID"""
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ids = []
            for row in reader:
                rid = row.get('RegistrationID', '')
                if rid.startswith('ANT25'):
                    try:
                        ids.append(int(rid.replace('ANT25', '')))
                    except ValueError:
                        pass
            return f"ANT25{(max(ids) + 1) if ids else 1:04d}"
    except:
        return 'ANT250001'

def save_registration(data):
    """Save registration data to CSV file"""
    try:
        now = datetime.now()
        registration_id = generate_registration_id()

        registration_data = [
            registration_id,
            data['fullname'].strip(),
            data['email'].strip().lower(),
            data['phone'].strip(),
            data['department'].strip(),
            data['year'].strip(),
            data.get('college', '').strip(),
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S')
        ]

        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(registration_data)

        return registration_id
    except Exception as e:
        print(f"Error saving registration: {str(e)}")
        return None

def get_all_registrations():
    """Get all registrations from CSV file"""
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

# Routes
@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = {
            'fullname': request.form.get('fullname', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'department': request.form.get('department', '').strip(),
            'year': request.form.get('year', '').strip(),
            'college': request.form.get('college', '').strip()
        }

        errors = []
        for field in REQUIRED_FIELDS:
            if not form_data[field]:
                errors.append(f"{field.title()} is required.")

        if form_data['email'] and not validate_email(form_data['email']):
            errors.append("Please enter a valid email address.")
        if form_data['phone'] and not validate_phone(form_data['phone']):
            errors.append("Phone number must be exactly 10 digits.")
        if form_data['email'] and email_exists(form_data['email']):
            errors.append("This email address is already registered.")
        if form_data['phone'] and phone_exists(form_data['phone']):
            errors.append("This phone number is already registered.")

        if errors:
            return render_template('register.html', title='Register', error=" ".join(errors), **form_data)

        registration_id = save_registration(form_data)
        if registration_id:
            flash(f'Registration successful! Your Registration ID is: {registration_id}', 'success')
            return redirect(url_for('thankyou'))
        else:
            return render_template('register.html', title='Register', error="Registration failed. Please try again.")

    return render_template('register.html', title='Register')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', title='Thank You')

@app.route('/admin')
def admin():
    registrations = get_all_registrations()
    return jsonify({
        'total_registrations': len(registrations),
        'registrations': registrations
    })

@app.route('/admin/download')
def download_registrations():
    try:
        registrations = get_all_registrations()
        return jsonify({
            'success': True,
            'message': f'Found {len(registrations)} registrations',
            'data': registrations
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Anantya 2025 website is running',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize application for start.py
def init_app():
    initialize_csv()
    print("Anantya 2025 website initialized successfully!")

if __name__ == '__main__':
    init_app()
    print("\n" + "=" * 50)
    print("ANANTYA 2025 - ACM PCCoE WEBSITE")
    print("=" * 50)
    print("Starting development server...")
    print("URL: http://localhost:5000")
    print("Admin API: http://localhost:5000/admin")
    print("Health Check: http://localhost:5000/health")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
