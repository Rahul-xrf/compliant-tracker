import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
    
    filtered_complaints = complaints.copy()
    
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
        filtered_complaints.sort(key=lambda x: priority_order[x['priority']])
    
    return render_template('admin.html', 
                         complaints=filtered_complaints,
                         current_filter=status_filter,
                         current_sort=sort_by)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        status = request.form['status']
        notes = request.form.get('notes', '')
        
        for complaint in complaints:
            if complaint['id'] == id:
                complaint['status'] = status
                complaint['notes'] = notes
                complaint['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                flash('Complaint updated successfully!', 'success')
                break
    except Exception as e:
        flash('Error updating complaint. Please try again.', 'error')
    return redirect(url_for('admin'))

# Temporary in-memory storage (we'll replace this with MySQL later)
complaints = []

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        department = request.form['department']
        category = request.form['category']
        description = request.form['description']
        file_url = None
        # Handle file upload
        if 'evidence' in request.files:
            file = request.files['evidence']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                else:
                    flash('File type not allowed. Please upload an image or PDF.', 'error')
                    return redirect(url_for('home'))
        # Handle "Other" category
        if category == 'Other':
            other_category = request.form.get('otherCategory')
            if other_category:
                category = f"Other: {other_category}"
        complaint = {
            'id': len(complaints) + 1,
            'name': name,
            'department': department,
            'category': category,
            'description': description,
            'status': 'Pending',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'priority': request.form.get('priority', 'Medium'),
            'file_url': file_url
        }
        complaints.append(complaint)
        flash('Complaint submitted successfully!', 'success')
    except Exception as e:
        flash('Error submitting complaint. Please try again.', 'error')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
