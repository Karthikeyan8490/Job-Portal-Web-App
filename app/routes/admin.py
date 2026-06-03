"""Admin Routes"""
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app import get_db_connection
from flask import current_app

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if session.get('user_role') != 'admin':
        return redirect(url_for('auth.index'))
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM users")
            users = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) AS c FROM job_listings")
            jobs = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) AS c FROM applications")
            apps = cur.fetchone()['c']
        return render_template('dashboard/admin.html',
                               total_users=users, total_jobs=jobs, total_apps=apps)
    finally:
        conn.close()
