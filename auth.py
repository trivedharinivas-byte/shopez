import os
import hashlib
from nicegui import app
import database

def hash_password(password: str) -> str:
    # 100,000 iterations is a secure standard for pbkdf2 with sha256
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}:{key.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, key_hex = stored_hash.split(':')
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return new_key == key
    except Exception:
        return False

def register_user(username, email, password):
    if not username or not email or not password:
        return False, "All fields are required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
        
    pwd_hash = hash_password(password)
    # The first registered user is automatically set to admin for convenience, 
    # others are normal users. Let's check if user table is empty.
    conn = database.get_db_connection()
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    
    is_admin = 1 if user_count == 0 else 0
    
    user_id = database.create_user(username, email, pwd_hash, is_admin)
    if user_id is None:
        return False, "Username already exists"
        
    return True, "Registration successful"

def login_user(username, password):
    user = database.get_user_by_username(username)
    if not user:
        return False, "Invalid username or password"
        
    if verify_password(password, user['password_hash']):
        # Set session details in nicegui storage
        app.storage.user['user_id'] = user['id']
        app.storage.user['username'] = user['username']
        app.storage.user['is_admin'] = bool(user['is_admin'])
        app.storage.user['logged_in'] = True
        return True, "Login successful"
        
    return False, "Invalid username or password"

def logout_user():
    app.storage.user.clear()

def is_logged_in() -> bool:
    return app.storage.user.get('logged_in', False)

def get_current_user_id():
    return app.storage.user.get('user_id')

def get_current_username():
    return app.storage.user.get('username', 'Guest')

def is_admin() -> bool:
    return app.storage.user.get('is_admin', False)
