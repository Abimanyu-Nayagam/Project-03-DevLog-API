# auth.py

import requests
import re
from utils import TOKEN_FILE, console

def register_user():
    """Register a new user."""
    url = "http://localhost:5000/register"

    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        res = requests.post(url, json={
            "email": email,
            "username": username,
            "password": password
        })

        data = res.json()

        if res.status_code == 201:
            print("Registration successful!")
        else:
            print("Registration failed:", data)

    except requests.exceptions.RequestException as e:
        print(f"Error during registration: {e}")


def login_user():
    """Login a user and store JWT token to file."""
    url = "http://localhost:5000/login"

    username_or_email = input("Enter username or email: ")
    password = input("Enter password: ")

    # Determine if input is email or username using regex validation
    email_pattern = r'^[\w\. ]+@[\w\. ]+\.\w+$'
    is_email = re.match(email_pattern, username_or_email) is not None
    payload = {
        "email" if is_email else "username": username_or_email,
        "password": password
    }

    try:
        res = requests.post(url, json=payload)

        data = res.json()

        if res.status_code == 200:
            access_token = data.get("access_token")
            try:
                TOKEN_FILE.write_text(access_token)
            except Exception:
                pass
            print("Login successful!")
            print(f"Token saved to {TOKEN_FILE}")
        else:
            print("Login failed:", data)

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")


def logout_user():
    """Clear saved token file."""
    try:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            print(f"Logged out and removed token file {TOKEN_FILE}")
        else:
            print("Logged out (no token file found)")
    except Exception as e:
        print(f"Logout error: {e}")


def get_token():
    """Read token from file if available."""
    try:
        if TOKEN_FILE.exists():
            return TOKEN_FILE.read_text().strip()
    except Exception:
        pass
    return ""
