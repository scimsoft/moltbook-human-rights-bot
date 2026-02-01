#!/usr/bin/env python3
"""
Setup script for Moltbook Bot
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file if it doesn't exist"""
    env_path = Path(".env")
    
    if env_path.exists():
        print(".env file already exists.")
        return
    
    print("Creating .env file...")
    with open(env_path, 'w') as f:
        f.write("""# Moltbook Bot Configuration

# Moltbook credentials
MOLTBOOK_USERNAME=your_username
MOLTBOOK_PASSWORD=your_password
MOLTBOOK_API_KEY=your_api_key

# Other configuration
POST_INTERVAL_MINUTES=60
MAX_POSTS_PER_DAY=10
""")
    
    print("Created .env file. Please update it with your actual credentials.")

def install_dependencies():
    """Install required dependencies"""
    import subprocess
    
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

def main():
    print("Setting up Moltbook Bot...")
    
    # Create .env file if needed
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    print("\nSetup complete!")
    print("To run the bot:")
    print("1. Edit the .env file with your credentials")
    print("2. Run: python main.py")

if __name__ == "__main__":
    main()