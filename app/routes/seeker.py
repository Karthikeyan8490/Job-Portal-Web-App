"""Job Seeker Routes"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import get_db_connection
from flask import current_app

seeker_bp = Blueprint('seeker', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'seeker':
            flash('Please log in as a job seeker.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@seeker_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.*, j.title, j.location, c.name AS company
                FROM applications a
                JOIN job_listings j ON a.job_id = j.id
                JOIN companies    c ON j.company_id = c.id
                WHERE a.user_id = %s ORDER BY a.applied_at DESC
            """, (session['user_id'],))
            applications = cur.fetchall()
        return render_template('dashboard/seeker.html', applications=applications)
    finally:
        conn.close()

@seeker_bp.route('/jobs')
def browse_jobs():
    search   = request.args.get('q', '')
    location = request.args.get('location', '')
    category = request.args.get('category', '')
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            query = """
                SELECT j.*, c.name AS company, c.location AS company_loc
                FROM job_listings j JOIN companies c ON j.company_id = c.id
                WHERE j.deadline >= CURDATE()
            """
            params = []
            if search:
                query += " AND (j.title LIKE %s OR j.description LIKE %s)"
                params += [f'%{search}%', f'%{search}%']
            if location:
                query += " AND j.location LIKE %s"
                params.append(f'%{location}%')
            if category:
                query += " AND j.category = %s"
                params.append(category)
            query += " ORDER BY j.id DESC"
            cur.execute(query, params)
            jobs = cur.fetchall()
        return render_template('jobs.html', jobs=jobs, search=search,
                               location=location, category=category)
    finally:
        conn.close()

@seeker_bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply(job_id):
    conn = get_db_connection(current_app)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM applications WHERE user_id=%s AND job_id=%s",
                        (session['user_id'], job_id))
            if cur.fetchone():
                flash('You have already applied for this job.', 'warning')
            else:
                cur.execute(
                    "INSERT INTO applications (user_id, job_id, status) VALUES (%s,%s,'pending')",
                    (session['user_id'], job_id)
                )
                conn.commit()
                flash('Application submitted successfully!', 'success')
    finally:
        conn.close()
    return redirect(url_for('seeker.dashboard'))
