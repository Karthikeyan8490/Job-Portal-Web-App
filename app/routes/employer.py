"""Employer Routes"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db_connection
from flask import current_app

employer_bp = Blueprint('employer', __name__)

def employer_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'employer':
            flash('Please log in as an employer.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@employer_bp.route('/dashboard')
@employer_required
def dashboard():
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT j.*, COUNT(a.id) AS total_applications
                FROM job_listings j
                JOIN companies c ON j.company_id = c.id
                LEFT JOIN applications a ON j.id = a.job_id
                WHERE c.user_id = %s
                GROUP BY j.id ORDER BY j.id DESC
            """, (session['user_id'],))
            listings = cur.fetchall()
        return render_template('dashboard/employer.html', listings=listings)
    finally:
        conn.close()

@employer_bp.route('/post-job', methods=['GET', 'POST'])
@employer_required
def post_job():
    if request.method == 'POST':
        conn = get_db_connection(current_app)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM companies WHERE user_id=%s", (session['user_id'],))
                company = cur.fetchone()
                if not company:
                    flash('Complete your company profile first.', 'warning')
                    return redirect(url_for('employer.dashboard'))
                cur.execute("""
                    INSERT INTO job_listings
                    (company_id, title, description, location, salary, category, deadline)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (company['id'],
                      request.form['title'], request.form['description'],
                      request.form['location'], request.form.get('salary', 0),
                      request.form['category'], request.form['deadline']))
                conn.commit()
                flash('Job posted successfully!', 'success')
                return redirect(url_for('employer.dashboard'))
        finally:
            conn.close()
    return render_template('dashboard/post_job.html')

@employer_bp.route('/applicants/<int:job_id>')
@employer_required
def applicants(job_id):
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.name, u.email, a.status, a.applied_at, a.id AS app_id
                FROM applications a JOIN users u ON a.user_id = u.id
                WHERE a.job_id = %s ORDER BY a.applied_at DESC
            """, (job_id,))
            apps = cur.fetchall()
        return render_template('dashboard/applicants.html', apps=apps, job_id=job_id)
    finally:
        conn.close()

@employer_bp.route('/update-status/<int:app_id>/<status>')
@employer_required
def update_status(app_id, status):
    if status not in ('pending', 'shortlisted', 'rejected'):
        flash('Invalid status.', 'danger')
        return redirect(url_for('employer.dashboard'))
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE applications SET status=%s WHERE id=%s", (status, app_id))
        conn.commit()
        flash(f'Status updated to {status}.', 'success')
    finally:
        conn.close()
    return redirect(request.referrer or url_for('employer.dashboard'))
