from src.database import Database
from datetime import datetime

class StatusManager:
    def __init__(self):
        self.db = Database()

    def get_current_status(self):
        """What are you doing right now?"""
        return self.db.get_current_status()

    def update_status(self, activity):
        """Set your activity"""
        self.db.update_status(activity)
        return {'status': 'updated', 'activity': activity}