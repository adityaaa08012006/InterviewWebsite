# Configuration file for Anantya 2025 Website

import os
from datetime import datetime

class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'anantya_2025_secret_key_acm_pccoe'

    # Event Configuration
    EVENT_NAME = "Anantya 2025"
    EVENT_ORGANIZATION = "ACM PCCoE Student Chapter"
    EVENT_DATES = "March 7-8, 2025"
    EVENT_VENUE = "PCCOE Campus, Nigdi, Pune"

    # Registration Configuration
    REGISTRATION_OPEN = True
    MAX_REGISTRATIONS = 500  # Set to None for unlimited

    # File Configuration
    DATA_DIR = "data"
    CSV_FILE = os.path.join(DATA_DIR, "registrations.csv")

    # Email Configuration (for future enhancements)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Admin Configuration
    ADMIN_EMAIL = "pccoeacm@gmail.com"

    # Validation Rules
    REQUIRED_FIELDS = ['fullname', 'email', 'phone', 'department', 'year']

    DEPARTMENTS = [
        "Computer Engineering",
        "Information Technology", 
        "Electronics & Telecommunication",
        "Mechanical Engineering",
        "Civil Engineering",
        "Electrical Engineering",
        "MCA",
        "MBA",
        "Other"
    ]

    YEARS_OF_STUDY = [
        "First Year",
        "Second Year", 
        "Third Year",
        "Final Year",
        "Post Graduate"
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    CSV_FILE = "test_registrations.csv"

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
