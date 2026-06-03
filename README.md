# 💼 Job Portal Web App

> **Full-Stack Web Application — Python Flask · MySQL · Bootstrap · REST APIs**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-black.svg)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)](https://mysql.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)

A fully functional **Job Portal Web Application** connecting job seekers with employers. Built with Python Flask on the backend and Bootstrap on the frontend, with MySQL for persistent storage.

---

## ✨ Features

### 👤 Job Seeker
- Register / Login with hashed passwords
- Browse & search job listings by title, location, category
- Apply to jobs with resume upload
- Track application status (Pending / Shortlisted / Rejected)
- Edit profile and skills

### 🏢 Employer
- Register company profile
- Post, edit, delete job listings
- View & manage applicants per listing
- Shortlist or reject candidates
- Dashboard with hiring statistics

### 🔧 Admin
- Manage all users, companies, and listings
- View platform-wide analytics
- Ban/unban accounts

---

## 🏗️ Project Structure

```
Job-Portal-Web-App/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy / raw JDBC models
│   ├── routes/
│   │   ├── auth.py          # Login, register, logout
│   │   ├── seeker.py        # Job seeker routes
│   │   ├── employer.py      # Employer routes
│   │   └── admin.py         # Admin routes
│   ├── templates/
│   │   ├── base.html        # Bootstrap layout
│   │   ├── index.html       # Landing page
│   │   ├── jobs.html        # Job listings
│   │   ├── job_detail.html  # Single job view
│   │   ├── dashboard/
│   │   │   ├── seeker.html
│   │   │   └── employer.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── db/
│   └── schema.sql           # Full MySQL schema
├── config.py                # App configuration
├── run.py                   # Entry point
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Schema

```sql
users          (id, name, email, password_hash, role, created_at)
companies      (id, user_id, name, description, website, location)
job_listings   (id, company_id, title, description, location, salary, category, deadline)
applications   (id, user_id, job_id, status, applied_at, resume_path)
skills         (id, user_id, skill_name)
```

---

## ⚙️ Setup

```bash
git clone https://github.com/Karthikeyan8490/Job-Portal-Web-App.git
cd Job-Portal-Web-App

python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

pip install -r requirements.txt

# Setup database
mysql -u root -p < db/schema.sql

# Configure credentials
cp config.py.example config.py
# Edit config.py with your MySQL details

python run.py
# Visit http://localhost:5000
```

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.9, Flask 2.3   |
| Database   | MySQL 8.0 + PyMySQL     |
| Frontend   | HTML5, Bootstrap 5.3    |
| Auth       | Flask-Login + Bcrypt    |
| Forms      | Flask-WTF + WTForms     |
| Upload     | Flask file handling     |

---

## 👨‍💻 Author

**Bukka Karthikeyan** — MVSR Engineering College, Hyderabad
