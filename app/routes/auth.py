"""Authentication Routes - Login, Register, Logout"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pymysql, bcrypt
from app import get_db_connection
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        role     = request.form['role']   # 'seeker' or 'employer'

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        try:
            conn = get_db_connection(current_app)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (name, email, password_hash, role) VALUES (%s,%s,%s,%s)",
                    (name, email, pw_hash, role)
                )
            conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except pymysql.IntegrityError:
            flash('Email already registered.', 'danger')
        finally:
            conn.close()
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        conn = get_db_connection(current_app)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cur.fetchone()
            if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
                session['user_id']   = user['id']
                session['user_name'] = user['name']
                session['user_role'] = user['role']
                flash(f"Welcome back, {user['name']}!", 'success')
                return redirect(url_for(f"{user['role']}.dashboard"))
            flash('Invalid email or password.', 'danger')
        finally:
            conn.close()
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.index'))
