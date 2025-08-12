# validations.py
import re
from data_utils import check_duplicate

# Email regex pattern (basic)
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# Phone should be exactly 10 digits
PHONE_REGEX = r'^\d{10}$'

def validate_form_data(full_name, email, phone, department, year):
    """
    Validate all fields from the registration form.
    Returns (True, None) if valid, otherwise (False, 'error message')
    """

    # Required fields check
    if not full_name.strip():
        return False, "Full name is required"

    if not email.strip():
        return False, "Email is required"

    if not phone.strip():
        return False, "Phone is required"

    if not department.strip() or department == "Select Department":
        return False, "Please select a department"

    if not year.strip() or year == "Select Year":
        return False, "Please select your year of study"

    # Pattern checks
    if not re.match(EMAIL_REGEX, email):
        return False, "Invalid email format"

    if not re.match(PHONE_REGEX, phone):
        return False, "Phone number must be exactly 10 digits"

    # Duplicate checks in CSV
    if check_duplicate(email=email):
        return False, "Email already registered"

    if check_duplicate(phone=phone):
        return False, "Phone number already registered"

    return True, None
