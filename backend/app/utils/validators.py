import re
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.extensions import db
from app.models.user import User

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PHONE_REGEX = r'^[6-9]\d{9}$'
PINCODE_REGEX = r'^[1-9][0-9]{5}$'

def validate_email(email):
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_phone(phone):
    if not phone:
        return True # phone is optional on register, but if provided must match
    cleaned = re.sub(r'[\s\-\+]', '', str(phone))
    if cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    return bool(re.match(PHONE_REGEX, cleaned))

def clean_phone(phone):
    if not phone:
        return None
    cleaned = re.sub(r'[\s\-\+]', '', str(phone))
    if cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    return cleaned

def validate_pincode(pincode):
    if not pincode:
        return False
    cleaned = re.sub(r'\s', '', str(pincode))
    return bool(re.match(PINCODE_REGEX, cleaned))

def validate_password_strength(password):
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

def admin_required():
    """
    Decorator for verifying that the current authenticated user has role='admin'
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = db.session.get(User, user_id)
            if not user or not user.is_active or user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Access denied: Administrator privileges required.'
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
