import sqlite3
from typing import List, Optional
import json

# Data Model: StudentProfile
class StudentProfile:
    def __init__(self, student_id: str, name: str, progress: dict, quiz_results: List[dict], chat_history: List[str]):
        self.student_id = student_id
        self.name = name
        self.progress = progress  # e.g., {module_id: percent_complete}
        self.quiz_results = quiz_results  # list of {quiz_id, score, timestamp}
        self.chat_history = chat_history  # list of chat messages

# Data Model: LearningContent
class LearningContent:
    def __init__(self, content_id: str, title: str, content_type: str, data: str, metadata: dict):
        self.content_id = content_id
        self.title = title
        self.content_type = content_type  # e.g., 'module', 'video', 'quiz', 'media'
        self.data = data  # could be text, file path, or binary
        self.metadata = metadata  # e.g., {duration, tags, etc.}

# SQLite Data Access Layer
class LocalDatabase:
    def __init__(self, db_path='akulearn_hub.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS student_profile (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            progress TEXT,
            quiz_results TEXT,
            chat_history TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS learning_content (
            content_id TEXT PRIMARY KEY,
            title TEXT,
            content_type TEXT,
            data TEXT,
            metadata TEXT
        )''')
        self.conn.commit()

    # CRUD for StudentProfile
    def add_student(self, profile: StudentProfile):
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO student_profile VALUES (?, ?, ?, ?, ?)''', (
            profile.student_id, profile.name,
            json.dumps(profile.progress),
            json.dumps(profile.quiz_results),
            json.dumps(profile.chat_history)
        ))
        self.conn.commit()

    def get_student(self, student_id: str) -> Optional[StudentProfile]:
        c = self.conn.cursor()
        c.execute('SELECT * FROM student_profile WHERE student_id=?', (student_id,))
        row = c.fetchone()
        if row:
            return StudentProfile(
                student_id=row[0], name=row[1],
                progress=json.loads(row[2]),
                quiz_results=json.loads(row[3]),
                chat_history=json.loads(row[4])
            )
        return None

    def update_student(self, profile: StudentProfile):
        self.add_student(profile)

    def delete_student(self, student_id: str):
        c = self.conn.cursor()
        c.execute('DELETE FROM student_profile WHERE student_id=?', (student_id,))
        self.conn.commit()

    # CRUD for LearningContent
    def add_content(self, content: LearningContent):
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO learning_content VALUES (?, ?, ?, ?, ?)''', (
            content.content_id, content.title, content.content_type,
            content.data, json.dumps(content.metadata)
        ))
        self.conn.commit()

    def get_content(self, content_id: str) -> Optional[LearningContent]:
        c = self.conn.cursor()
        c.execute('SELECT * FROM learning_content WHERE content_id=?', (content_id,))
        row = c.fetchone()
        if row:
            return LearningContent(
                content_id=row[0], title=row[1], content_type=row[2],
                data=row[3], metadata=json.loads(row[4])
            )
        return None

    def update_content(self, content: LearningContent):
        self.add_content(content)

    def delete_content(self, content_id: str):
        c = self.conn.cursor()
        c.execute('DELETE FROM learning_content WHERE content_id=?', (content_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
