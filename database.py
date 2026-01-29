import sqlite3
from datetime import datetime

class AttendanceDatabase:
    def __init__(self):
        self.db_file = 'attendance.db'
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                UNIQUE(student_id, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_student(self, roll_number, name, email):
        """Add a new student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO students (roll_number, name, email) VALUES (?, ?, ?)',
                (roll_number, name, email)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_students(self):
        """Get all students"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY roll_number')
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    
    def get_student_by_id(self, student_id):
        """Get student by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return dict(student) if student else None
    
    def delete_student(self, student_id):
        """Delete a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return True
    
    def mark_attendance(self, student_id, date, status, remarks=''):
        """Mark attendance for a student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO attendance (student_id, date, status, remarks) 
                   VALUES (?, ?, ?, ?)''',
                (student_id, date, status, remarks)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
    
    def get_attendance_by_date(self, date):
        """Get attendance records for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT a.*, s.name, s.roll_number FROM attendance a
               JOIN students s ON a.student_id = s.id
               WHERE a.date = ?
               ORDER BY s.roll_number''',
            (date,)
        )
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records
    
    def get_student_attendance(self, student_id):
        """Get attendance history for a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC',
            (student_id,)
        )
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records
    
    def get_attendance_summary(self):
        """Get attendance summary statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get total students
        cursor.execute('SELECT COUNT(*) as total FROM students')
        total_students = cursor.fetchone()['total']
        
        # Get today's attendance
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) as present FROM attendance WHERE date = ? AND status = ?', (today, 'Present'))
        present_today = cursor.fetchone()['present']
        
        cursor.execute('SELECT COUNT(*) as absent FROM attendance WHERE date = ? AND status = ?', (today, 'Absent'))
        absent_today = cursor.fetchone()['absent']
        
        conn.close()
        
        return {
            'total_students': total_students,
            'present_today': present_today,
            'absent_today': absent_today,
            'not_marked': total_students - present_today - absent_today
        }