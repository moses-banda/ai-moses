import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="ai_moses.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self._connect()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                phone_number TEXT PRIMARY KEY,
                name TEXT,
                relationship TEXT,
                tone TEXT,
                topics TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT,
                updated_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS call_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                call_sid TEXT,
                incoming_text TEXT,
                ai_response TEXT,
                summary_text TEXT,
                summary_audio_path TEXT,
                timestamp TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS voice_recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                call_sid TEXT,
                file_path TEXT,
                duration REAL,
                transcription TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()

    def get_caller_profile(self, phone_number):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT * FROM contacts WHERE phone_number = ?", (phone_number,))
        row = c.fetchone()
        conn.close()

        if not row:
            return {
                "name": "Unknown Caller",
                "relationship": "unknown",
                "tone": "neutral",
                "topics": ""
            }

        return {
            "phone_number": row[0],
            "name": row[1],
            "relationship": row[2],
            "tone": row[3],
            "topics": row[4],
        }

    def add_caller_profile(self, phone_number, name, relationship, tone, topics):
        conn = self._connect()
        c = conn.cursor()

        try:
            c.execute("""
                INSERT OR REPLACE INTO contacts (phone_number, name, relationship, tone, topics)
                VALUES (?, ?, ?, ?, ?)
            """, (phone_number, name, relationship, tone, topics))

            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def get_all_contacts(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT * FROM contacts")
        rows = c.fetchall()
        conn.close()

        return [
            {
                "phone_number": row[0],
                "name": row[1],
                "relationship": row[2],
                "tone": row[3],
                "topics": row[4]
            }
            for row in rows
        ]

    def get_current_status(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT activity, updated_at FROM status ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()

        if not row:
            return {"activity": "Available", "updated_at": None}

        return {"activity": row[0], "updated_at": row[1]}

    def update_status(self, activity):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO status (activity, updated_at)
            VALUES (?, ?)
        """, (activity, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True

    def log_call(self, phone_number, call_sid, incoming_text, ai_response):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO call_history (phone_number, call_sid, incoming_text, ai_response, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (phone_number, call_sid, incoming_text, ai_response, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def update_call_summary(self, call_sid, summary_text, summary_audio_path):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            UPDATE call_history 
            SET summary_text = ?, summary_audio_path = ?
            WHERE call_sid = ?
        """, (summary_text, summary_audio_path, call_sid))
        conn.commit()
        conn.close()

    def get_call_history(self, phone_number, limit=10):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT call_sid, incoming_text, ai_response, timestamp, summary_text, summary_audio_path
            FROM call_history
            WHERE phone_number = ?
            ORDER BY id DESC
            LIMIT ?
        """, (phone_number, limit))
        rows = c.fetchall()
        conn.close()

        return [
            {
                "call_sid": row[0],
                "incoming_text": row[1],
                "ai_response": row[2],
                "timestamp": row[3],
                "summary_text": row[4],
                "summary_audio_path": row[5]
            }
            for row in rows
        ]

    def add_voice_recording(self, phone_number, call_sid, file_path, duration, transcription):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO voice_recordings (phone_number, call_sid, file_path, duration, transcription, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            phone_number,
            call_sid,
            file_path,
            duration,
            transcription,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        return True

    def get_recent_calls(self, limit=10):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT phone_number, call_sid, incoming_text, ai_response, timestamp, summary_text, summary_audio_path
            FROM call_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()

        return [
            {
                "phone_number": row[0],
                "call_sid": row[1],
                "incoming_text": row[2],
                "ai_response": row[3],
                "timestamp": row[4],
                "summary_text": row[5],
                "summary_audio_path": row[6]
            }
            for row in rows
        ]