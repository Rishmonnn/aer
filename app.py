from flask import Flask, render_template, request, jsonify, session, redirect, url_for # pyright: ignore[reportMissingImports]
from functools import wraps
import os
from config import get_config

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Load configuration
config_env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(get_config(config_env))

# Mock database data - replace with actual database queries
FACULTY_DATA = {
    'classes': 3,
    'total_students': 45,
    'grading_status': '67%'
}

CLASS_DATA = [
    {'id': 1, 'code': 'CE101', 'name': 'Introduction to Civil Engineering', 'students': 35},
    {'id': 2, 'code': 'CE102', 'name': 'Structural Analysis', 'students': 40},
    {'id': 3, 'code': 'CE103', 'name': 'Fluid Mechanics', 'students': 38}
]

def login_required(f):
    """Decorator to enforce login requirement"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Homepage - Login page"""
    if 'user' in session:
        # Redirect to appropriate dashboard if already logged in
        if session.get('role') == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        elif session.get('role') == 'head':
            return redirect(url_for('program_head_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login submissions"""
    email = request.form.get('email', '').lower()
    password = request.form.get('password', '')
    role = request.form.get('role', '')
    
    # Basic validation
    if not email or not password or not role:
        return redirect(url_for('index'))
    
    # Mock authentication - replace with real database/auth system
    if role == 'faculty' and 'faculty' in email:
        session['user'] = email
        session['role'] = 'faculty'
        return redirect(url_for('faculty_dashboard'))
    elif role == 'head' and 'head' in email:
        session['user'] = email
        session['role'] = 'head'
        return redirect(url_for('program_head_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/faculty')
@login_required
def faculty_dashboard():
    """Faculty dashboard page"""
    if session.get('role') != 'faculty':
        return redirect(url_for('index'))
    
    context = {
        'pageTitle': 'Faculty Dashboard',
        'pageStyles': ['dashboard.css', 'faculty.css'],
        'pageScripts': ['faculty.js', 'faculty-grading.js', 'faculty-classes.js', 'faculty-inc.js'],
        'user_name': session.get('user', 'Faculty'),
        'stats': FACULTY_DATA
    }
    return render_template('faculty.html', **context)

@app.route('/program-head')
@login_required
def program_head_dashboard():
    """Program head dashboard page"""
    if session.get('role') != 'head':
        return redirect(url_for('index'))
    
    context = {
        'pageTitle': 'Program Head Dashboard',
        'user_name': session.get('user', 'Program Head'),
        'pageStyles': ['program-head.css'],
        'pageScripts': ['program-head.js']
    }
    return render_template('program-head.html', **context)

# ==================== API Routes ====================

@app.route('/api/faculty/classes', methods=['GET'])
@login_required
def get_faculty_classes():
    """Get list of faculty classes"""
    return jsonify(CLASS_DATA)

@app.route('/api/faculty/grading/<int:class_id>', methods=['GET'])
@login_required
def get_grading_records(class_id):
    """Get grading records for a specific class"""
    records = [
        {'id': 1, 'name': 'Student One', 'p1': 85, 'p2': 90, 'p3': 88, 'final': 87.7},
        {'id': 2, 'name': 'Student Two', 'p1': 78, 'p2': 82, 'p3': 80, 'final': 80},
        {'id': 3, 'name': 'Student Three', 'p1': 92, 'p2': 88, 'p3': 95, 'final': 91.7},
    ]
    return jsonify(records)

@app.route('/api/faculty/inc', methods=['GET'])
@login_required
def get_inc_requests():
    """Get incomplete (INC) approval requests"""
    inc_requests = [
        {'id': 1, 'student_name': 'Juan Dela Cruz', 'subject': 'CE101', 'status': 'pending'},
        {'id': 2, 'student_name': 'Maria Santos', 'subject': 'CE102', 'status': 'pending'},
    ]
    return jsonify(inc_requests)

@app.route('/api/faculty/inc/<int:inc_id>/approve', methods=['POST'])
@login_required
def approve_inc(inc_id):
    """Approve an INC request"""
    return jsonify({'status': 'success', 'message': f'INC {inc_id} approved'})

@app.route('/api/faculty/inc/<int:inc_id>/deny', methods=['POST'])
@login_required
def deny_inc(inc_id):
    """Deny an INC request"""
    return jsonify({'status': 'success', 'message': f'INC {inc_id} denied'})

@app.route('/api/faculty/grades/<int:class_id>/<int:student_id>', methods=['POST'])
@login_required
def update_grade(class_id, student_id):
    """Update a student's grade"""
    data = request.get_json()
    period = data.get('period')  # p1, p2, p3, final
    grade = data.get('grade')
    
    return jsonify({'status': 'success', 'message': f'Grade updated for student {student_id}'})

# ==================== Program Head API Routes ====================

@app.route('/api/enrollment', methods=['POST'])
@login_required
def enroll_students():
    """Handle bulk enrollment from file"""
    return jsonify({'status': 'success', 'message': 'Enrollment data processed'})

@app.route('/api/advising', methods=['GET'])
@login_required
def get_advising():
    """Get list of students requiring advising"""
    advising_list = [
        {'id': 1, 'name': 'Juan Dela Cruz', 'program': 'Civil Engineering', 'status': 'pending'},
        {'id': 2, 'name': 'Maria Santos', 'program': 'Mechanical Engineering', 'status': 'active'},
    ]
    return jsonify(advising_list)

@app.route('/api/advising/<int:student_id>/advise', methods=['POST'])
@login_required
def advise_student(student_id):
    """Record advising for a student"""
    return jsonify({'status': 'success', 'message': f'Student {student_id} advised'})

@app.route('/api/retention', methods=['GET'])
@login_required
def get_retention_data():
    """Get retention and advising data"""
    retention_data = {
        'good': 45,
        'warning': 12,
        'probation': 8,
        'critical': 3,
        'students': [
            {'id': 1, 'name': 'John Doe', 'program': 'CEA', 'year': '3rd', 'gwa': 3.5, 'trend': 'up', 'status': 'Good Standing', 'statusClass': 'good'},
            {'id': 2, 'name': 'Jane Smith', 'program': 'CEA', 'year': '2nd', 'gwa': 2.8, 'trend': 'down', 'status': 'Warning', 'statusClass': 'warning'},
        ]
    }
    return jsonify(retention_data)

@app.route('/api/student/<int:student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    """Get detailed student information"""
    student = {
        'id': student_id,
        'name': 'Sample Student',
        'program': 'Civil Engineering',
        'gwa': 3.2,
        'status': 'Good Standing',
        'year': '3rd'
    }
    return jsonify(student)

@app.route('/api/retention/search', methods=['GET'])
@login_required
def search_retention():
    """Search retention data"""
    query = request.args.get('query', '')
    retention_data = {
        'good': 45,
        'warning': 12,
        'probation': 8,
        'critical': 3,
        'students': []
    }
    return jsonify(retention_data)

@app.route('/api/enlistment', methods=['GET'])
@login_required
def get_enlistment():
    """Get enlistment data"""
    enlistment_list = [
        {'id': 1, 'course': 'CE101', 'section': 'A', 'enlisted': 35},
        {'id': 2, 'course': 'CE102', 'section': 'B', 'enlisted': 40},
    ]
    return jsonify(enlistment_list)

@app.route('/api/enlistment/<int:enlist_id>/approve', methods=['POST'])
@login_required
def approve_enlistment(enlist_id):
    """Approve an enlistment"""
    return jsonify({'status': 'success', 'message': f'Enlistment {enlist_id} approved'})

@app.route('/api/classrecords', methods=['GET'])
@login_required
def get_classrecords():
    """Get class records"""
    records = [
        {'id': 1, 'course': 'CE101', 'instructor': 'Engr. Juan', 'term': 'AY 2025-2026 1st', 'students': []},
        {'id': 2, 'course': 'CE102', 'instructor': 'Engr. Maria', 'term': 'AY 2025-2026 1st', 'students': []},
    ]
    return jsonify(records)

@app.route('/api/classrecords/<int:class_id>', methods=['GET'])
@login_required
def get_classrecord(class_id):
    """Get specific class record"""
    record = {
        'id': class_id,
        'course': f'CE{100+class_id}',
        'instructor': 'Engr. Sample',
        'term': 'AY 2025-2026 1st',
        'students': [{'id': 1, 'name': 'Student 1'}, {'id': 2, 'name': 'Student 2'}]
    }
    return jsonify(record)

@app.route('/api/schedules', methods=['GET'])
@login_required
def get_schedules():
    """Get schedules"""
    schedules = [
        {'id': 1, 'title': 'Class Schedule A', 'times': 'MWF 9:00-10:30'},
        {'id': 2, 'title': 'Class Schedule B', 'times': 'TTh 2:00-3:30'},
    ]
    return jsonify(schedules)

@app.route('/api/schedules/<int:schedule_id>', methods=['PUT'])
@login_required
def update_schedule(schedule_id):
    """Update a schedule"""
    data = request.get_json()
    title = data.get('title', '')
    return jsonify({'status': 'success', 'message': f'Schedule {schedule_id} updated'})

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index')), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return redirect(url_for('index')), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='127.0.0.1', port=5000)
