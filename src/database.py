import psycopg2
from psycopg2.extras import RealDictCursor
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
    
    def get_caller_profile(self, phone_number):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM caller_profiles WHERE phone_number = %s",
                (phone_number,)
            )
            return cur.fetchone() or {}
    
    def get_current_status(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT activity, updated_at FROM status ORDER BY updated_at DESC LIMIT 1"
            )
            return cur.fetchone() or {'activity': 'Busy'}
    
    def update_status(self, activity):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO status (activity) VALUES (%s)",
                (activity,)
            )
            self.conn.commit()