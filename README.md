# 📚 Attendance Tracker

A comprehensive web-based attendance management system built with Python and Flask. Track student attendance, generate reports, and manage student records efficiently.

## Features

✨ **Core Features:**
- 👥 Student management (add, view, delete)
- 📋 Mark daily attendance
- 📊 Attendance reports and analytics
- 📈 Attendance percentage calculations
- 🔍 View individual student attendance history
- 💾 SQLite database for persistent storage
- 🎨 Clean and intuitive web interface

## Tech Stack

- **Backend:** Python 3.x with Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework:** Flask with SQLAlchemy ORM

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd c:\Users\sinch\OneDrive\Desktop\4MH23CS153\Attendance-tracker
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask Development Server
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

### Default Access
- Open your web browser
- Navigate to `http://localhost:5000`
- The application is ready to use!

## Project Structure

```
Attendance-tracker/
├── app.py                 # Main Flask application
├── database.py            # Database operations and models
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── templates/             # HTML templates
    ├── base.html          # Base template with styling
    ├── index.html         # Dashboard
    ├── students.html      # Student list
    ├── add_student.html   # Add new student form
    ├── attendance.html    # Mark attendance page
    ├── reports.html       # Attendance reports
    └── student_detail.html # Individual student details
```

## Usage Guide

### 1. **Adding Students**
- Navigate to "Students" → "Add Student"
- Enter roll number, name, and email
- Click "Add Student"

### 2. **Marking Attendance**
- Go to "Mark Attendance"
- Select the date (defaults to today)
- Mark each student as: Present, Absent, or Leave
- Add remarks if needed
- Click "Save Attendance"

### 3. **Viewing Reports**
- Go to "Reports"
- View attendance statistics for all students
- See attendance percentage and eligibility status
- Status indicators:
  - ✓ **Pass:** Attendance ≥ 75%
  - ⚠ **Warning:** Attendance 50-74%
  - ✗ **At Risk:** Attendance < 50%

### 4. **Student Details**
- Click "View" on any student in the Students list
- See complete attendance history
- View attendance summary and statistics

## Database Schema

### Students Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| roll_number | TEXT | Unique roll number |
| name | TEXT | Student name |
| email | TEXT | Student email (optional) |
| created_at | TIMESTAMP | Registration date |

### Attendance Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | INTEGER | Foreign key to students |
| date | TEXT | Attendance date |
| status | TEXT | Present/Absent/Leave |
| remarks | TEXT | Additional remarks |
| created_at | TIMESTAMP | Record creation date |

## API Endpoints

### GET Endpoints
- `/` - Dashboard
- `/students` - Student list
- `/attendance` - Mark attendance page
- `/reports` - Attendance reports
- `/student/<id>` - Student details
- `/api/attendance-date?date=YYYY-MM-DD` - Get attendance for specific date

### POST Endpoints
- `/add-student` - Add new student
- `/delete-student/<id>` - Delete student
- `/api/mark-attendance` - Save attendance record

## Features Explanation

### Dashboard
- Quick overview of today's attendance
- Total student count
- Present/Absent/Leave statistics
- Quick access to mark today's attendance

### Student Management
- Add students with roll number and email
- View all students in a table
- Delete student records (cascades attendance records)
- Click on student to see full details

### Attendance Marking
- Calendar date picker for flexible date selection
- Mark attendance for all students at once
- Add remarks for absence/leave
- Auto-load previous attendance for editing

### Reports & Analytics
- Comprehensive attendance statistics
- Visual progress bars for attendance percentage
- Automatic status indication (Pass/Warning/At Risk)
- Sort by any column for better analysis

## Configuration

Edit `app.py` to customize:

```python
# Change the secret key for production
app.secret_key = 'your-secret-key-change-this'

# Change Flask settings
app.run(debug=True, host='localhost', port=5000)
```

## Tips & Best Practices

1. **Data Backup:** Regularly backup the `attendance.db` file
2. **Multiple Dates:** Use the date picker to mark attendance for past/future dates
3. **Remarks:** Always add remarks for leave/absent to maintain records
4. **Reports:** Check reports regularly to identify at-risk students
5. **Security:** Change the secret key before deploying to production

## Troubleshooting

### Port Already in Use
If port 5000 is in use, edit `app.py`:
```python
app.run(debug=True, host='localhost', port=5001)
```

### Database Issues
Delete `attendance.db` and restart the app to reinitialize the database.

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Future Enhancements

- 📧 Email notifications for low attendance
- 📱 Mobile app support
- 🔐 User authentication and roles
- 📸 Biometric integration
- 📥 CSV import/export
- 📅 Scheduled reports
- 🔔 Automated alerts

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue or contact the development team.

---

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Author:** Attendance Tracker Team
"# Attendance-tracker" 
