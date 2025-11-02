# compliant-tracker
# 🚦 Complaint Tracker System  
A **cloud-based Flask web application** that allows students to submit and track complaints while admins can manage, update, and resolve them efficiently.  
Built with **Flask**, **MySQL (AWS RDS)**, **Docker**, and **GitHub Actions CI/CD**, it’s fully deployable on **AWS EC2**.

---

## 🌟 Features  
- 🎓 Student Dashboard – Submit and track complaints easily  
- 🧑‍💼 Admin Panel – Manage complaints, update status, and resolve issues  
- 📬 Email Notifications – Sends automatic emails for submission and updates  
- ☁️ Cloud Database – MySQL hosted on AWS RDS  
- 🐳 Fully Dockerized – Runs anywhere, production-ready  
- 🔁 CI/CD – Automatic deployment via GitHub Actions  
- 🔒 Secure – Environment variables & GitHub Secrets for sensitive data  

---

## ⚙️ Tech Stack  

| Layer | Tools Used |
|-------|-------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask (Python), Flask-Login |
| Database | AWS RDS (MySQL) |
| Cloud Hosting | AWS EC2 |
| DevOps | Docker, GitHub Actions |
| Version Control | Git & GitHub |
| Email Service | Gmail SMTP (App Password) |

---

## 🗂️ Project Structure  

compliant-tracker/
│
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
├── Dockerfile # Docker build recipe
├── .dockerignore # Ignore unnecessary files
├── templates/ # HTML templates
├── static/ # CSS, JS, and images
└── .github/workflows/ # GitHub Actions workflow


---

## 🚀 Run Locally (Using Docker)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/compliant-tracker.git
cd compliant-tracker

# 2. Create .env file
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
TRACKER_EMAIL=your_email@gmail.com
TRACKER_EMAIL_PASSWORD=your_gmail_app_password
SECRET_KEY=random_secret_key

# 3. Build & run container
docker build -t complaint-tracker .
docker run -d -p 5000:5000 --env-file .env complaint-tracker

# Access the app
http://localhost:5000


☁️ Deploy to AWS EC2 (Production)

SSH into your EC2 instance

Clone your repo or use GitHub Actions for auto-deployment

Build and run container:

docker build -t complaint-tracker .
docker run -d -p 5000:5000 --env-file .env complaint-tracker


Visit your app:
http://<your-ec2-public-ip>:5000

🔄 CI/CD with GitHub Actions

Trigger: On every push to main branch

What happens:
✅ GitHub Action connects to EC2 via SSH
✅ Copies updated code
✅ Builds a new Docker image
✅ Stops the old container
✅ Runs the latest version automatically

Once configured, your deployment is fully automated! ⚡

🔐 Security & Secrets

.env file is ignored in .gitignore

Use GitHub Secrets:

EC2_HOST

EC2_USER

EC2_SSH_KEY

Keep Gmail App password and DB credentials safe in environment variables

📬 Email Notifications

Uses Gmail SMTP (App Password)

Sends email when:

A student submits a complaint

The admin updates the complaint (In Progress / Resolved)

Example:

“Your complaint regarding the hostel issue has been resolved. Thank you for your patience!”

🛠️ Useful Docker Commands
# Build Docker image
docker build -t complaint-tracker .

# Run container
docker run -d -p 5000:5000 --env-file .env complaint-tracker

# Stop all running containers
docker stop $(docker ps -q)

# Clean up unused images & containers
docker system prune -f

🧩 Future Enhancements

📊 Complaint Statistics Dashboard (Chart.js)

⚙️ Terraform for Infrastructure Automation

🌐 Nginx reverse proxy + HTTPS (SSL)

🔐 JWT-based Admin Authentication

🧠 Setup for New Developers

If you’re a new developer, recruiter, or reviewer, you can test this project easily — no AWS setup needed.

🪜 Steps:

Clone this repo

Install Python (3.8 or higher)

In your terminal:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Create a local .env file:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=complaints
TRACKER_EMAIL=your_gmail@gmail.com
TRACKER_EMAIL_PASSWORD=your_gmail_app_password
SECRET_KEY=secret123


Start the app:

flask run


Open http://127.0.0.1:5000 in your browser

You’ll see the Complaint Tracker dashboard locally without any cloud setup.

📄 License

MIT License

📣 Credits

Flask

Gunicorn

Docker

GitHub Actions

AWS