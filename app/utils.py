from app import db
from app.models import ActivityLog
from flask_login import current_user

def log_activity(action, details=None):
    if current_user.is_authenticated:
        log = ActivityLog(user_id=current_user.id, action=action, details=details)
        db.session.add(log)
        db.session.commit()

def parse_college_id(cid_str):
    """Parses 'CIDA001' or '1' into integer 1. Returns None if invalid."""
    if not cid_str:
        return None
    try:
        clean_str = str(cid_str).strip().upper()
        if clean_str.startswith('CIDA'):
            clean_str = clean_str[4:]
        return int(clean_str)
    except ValueError:
        return None

def format_college_id(cid_int):
    """Formats integer 1 into 'CIDA001'."""
    if cid_int is None:
        return "N/A"
    return f"CIDA{cid_int:03d}"
