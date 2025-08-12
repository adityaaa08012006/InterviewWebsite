# data_utils.py
import csv
import os
from datetime import datetime

# Create a dedicated "data" folder if it doesn't exist
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

CSV_FILE = os.path.join(DATA_DIR, "registrations.csv")

CSV_HEADERS = [
    "RegistrationID", "FullName", "Email", "Phone",
    "Department", "Year", "College", "Timestamp"
]

def ensure_csv_exists():
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

def generate_reg_id():
    """Generate a unique registration ID like ANT250001."""
    ensure_csv_exists()
    with open(CSV_FILE, 'r', encoding='utf-8') as file:
        row_count = sum(1 for _ in file) - 1  # excluding header
    return f"ANT25{row_count + 1:04d}"

def save_registration(full_name, email, phone, department, year, college=""):
    """Save a single registration entry to CSV."""
    ensure_csv_exists()
    reg_id = generate_reg_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([reg_id, full_name, email, phone, department, year, college, timestamp])
    return reg_id

def check_duplicate(email=None, phone=None):
    """Check if email or phone already exists in CSV."""
    ensure_csv_exists()
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if email and row["Email"].lower() == email.lower():
                return True
            if phone and row["Phone"] == phone:
                return True
    return False

def get_all_registrations():
    """Read all registrations from CSV."""
    ensure_csv_exists()
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)
