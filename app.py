from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import AttendanceDatabase
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
db = AttendanceDatabase()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index')), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    flash('An error occurred. Please try again.', 'error')
    return redirect(url_for('index')), 500

@app.route('/')
def index():
    """Dashboard home page"""
    students = db.get_all_students()
    summary = db.get_attendance_summary()
    today = datetime.now().strftime('%Y-%m-%d')
    today_attendance = db.get_attendance_by_date(today)
    
    return render_template('index.html', 
                         students=students, 
                         summary=summary,
                         today=today,
                         today_attendance=today_attendance)

@app.route('/students')
def students():
    """View all students"""
    all_students = db.get_all_students()
    return render_template('students.html', students=all_students)

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not all([roll_number, name, email]):
            flash('All fields are required!', 'error')
            return render_template('add_student.html')
        
        if db.add_student(roll_number, name, email):
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('students'))
        else:
            flash('Error: Roll number already exists!', 'error')
    
    return render_template('add_student.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    """Mark attendance"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        date = request.form.get('date')
        status = request.form.get('status')
        remarks = request.form.get('remarks', '')
        
        if not all([student_id, date, status]):
            flash('Missing required fields!', 'error')
            return redirect(url_for('attendance'))
        
        if db.mark_attendance(student_id, date, status, remarks):
            flash('Attendance marked successfully!', 'success')
        else:
            flash('Error marking attendance!', 'error')
        
        return redirect(url_for('attendance'))
    
    students = db.get_all_students()
    today = datetime.now().strftime('%Y-%m-%d')
    today_attendance = db.get_attendance_by_date(today)
    
    attendance_dict = {att['student_id']: att for att in today_attendance}
    
    return render_template('attendance.html', 
                         students=students,
                         today=today,
                         attendance_dict=attendance_dict)

@app.route('/api/mark-attendance', methods=['POST'])
def api_mark_attendance():
    """API endpoint to mark attendance"""
    try:
        data = request.json
        student_id = data.get('student_id')
        date = data.get('date')
        status = data.get('status')
        remarks = data.get('remarks', '')
        
        if not all([student_id, date, status]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        if db.mark_attendance(student_id, date, status, remarks):
            return jsonify({'success': True, 'message': 'Attendance marked successfully'})
        else:
            return jsonify({'success': False, 'message': 'Error marking attendance'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/reports')
def reports():
    """Attendance reports and analytics"""
    summary = db.get_attendance_summary()
    return render_template('reports.html', summary=summary)

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """View student details and attendance history"""
    student = db.get_student_by_id(student_id)
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('students'))
    
    attendance_records = db.get_student_attendance(student_id)
    return render_template('student_detail.html', 
                         student=student, 
                         attendance_records=attendance_records)

@app.route('/delete-student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete a student"""
    student = db.get_student_by_id(student_id)
    if student:
        db.delete_student(student_id)
        flash(f'Student {student["name"]} deleted successfully!', 'success')
    else:
        flash('Student not found!', 'error')
    
    return redirect(url_for('students'))

@app.route('/api/attendance-date', methods=['GET'])
def api_attendance_date():
    """API endpoint to get attendance for a specific date"""
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Date parameter required'}), 400
    
    attendance = db.get_attendance_by_date(date)
    return jsonify(attendance)

if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        use_reloader=False,
        threaded=True
    )