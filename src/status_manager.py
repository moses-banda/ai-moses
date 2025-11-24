from src.database import Database
from datetime import datetime

db = Database()

def get_current_status():
    """What are you doing right now?"""
    return db.get_current_status()

def update_status(activity):
    """Set your activity"""
    db.update_status(activity)
    return {'status': 'updated', 'activity': activity}