#!/usr/bin/env python3
# Startup script for Anantya 2025 Website

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    os.makedirs("data", exist_ok=True)
    print("✅ Directories created")

def main():
    """Main startup function"""
    print("🚀 Starting Anantya 2025 Website Setup")
    print("="*50)

    check_python_version()
    install_requirements()
    create_directories()

    print("="*50)
    print("✅ Setup complete! Starting the website...")
    print("🌐 Website will be available at: http://localhost:5000")
    print("⚡ Press Ctrl+C to stop the server")
    print("="*50)

    # Import and run the Flask app
    from app import app, init_app
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
