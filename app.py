import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory users (admin only)
users = {
    'admin': {'password': 'adminpass', 'role': 'admin'}
}

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = users.get(user_id)
    if user:
        return User(user_id, user['role'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            login_user(User(username, user['role']))
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# MySQL connection setup
conn = mysql.connector.connect(
    host="complaint-db.cc7okgok4f7i.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Alienx2357",
    database="complaint_system"
)

# Protect admin route
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Admins only!', 'error')
        return redirect(url_for('login'))
    search_query = request.args.get('search', '').lower()
    status_filter = request.args.get('status_filter', 'all')
    sort_by = request.args.get('sort_by', 'timestamp')

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    cursor.close()

    filtered_complaints = complaints
    # Search functionality
    if search_query:
        filtered_complaints = [
            c for c in filtered_complaints
            if search_query in c['name'].lower() or
               search_query in c['department'].lower() or
               search_query in c['description'].lower()
        ]
    # Status filter
    if status_filter != 'all':
        filtered_complaints = [
            c for c in filtered_complaints
            if c['status'] == status_filter
        ]
    # Sorting
    if sort_by == 'timestamp':
        filtered_complaints.sort(key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == 'priority':
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        filtered_complaints.sort(key=lambda x: priority_order.get(x['priority'], 3))
    return render_template('admin.html', 
                         complaints=filtered_complaints,
                         current_filter=status_filter,
                         current_sort=sort_by)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        status = request.form['status']
        notes = request.form.get('notes', '')
        cursor = conn.cursor()
        sql = """
            UPDATE complaints SET status=%s, notes=%s, last_updated=NOW() WHERE id=%s
        """
        values = (status, notes, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        flash('Complaint updated successfully!', 'success')
    except Exception as e:
        flash('Error updating complaint. Please try again.', 'error')
    return redirect(url_for('admin'))

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/complaint')
def complaint():
    return render_template('index.html')

# Remove SQLAlchemy Complaint model and db usage
# Restore in-memory complaints list
# complaints = [] # This line is no longer needed as complaints are fetched from DB

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        department = request.form['department']
        category = request.form['category']
        description = request.form['description']
        priority = request.form.get('priority', 'Medium')
        file_url = None
        # Handle file upload (existing code)
        if 'evidence' in request.files:
            file = request.files['evidence']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    file.seek(0, 2)  # Seek to end of file
                    file_length = file.tell()
                    file.seek(0)  # Reset pointer
                    if file_length > app.config['MAX_CONTENT_LENGTH']:
                        flash('File is too large. Maximum allowed size is 10 MB.', 'error')
                        return redirect(url_for('complaint'))
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                else:
                    flash('File type not allowed. Please upload an image or PDF.', 'error')
                    return redirect(url_for('complaint'))
        # Handle "Other" category
        if category == 'Other':
            other_category = request.form.get('otherCategory')
            if other_category:
                category = f"Other: {other_category}"
        cursor = conn.cursor()
        sql = """
            INSERT INTO complaints (name, department, category, description, priority, status, file_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, department, category, description, priority, 'Pending', file_url)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        flash('Complaint submitted successfully!', 'success')
    except Exception as e:
        print('Error in /submit:', e)
        flash('Error submitting complaint. Please try again.', 'error')
    return redirect(url_for('complaint'))

@app.route('/back-from-complaint')
def back_from_complaint():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
