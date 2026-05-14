import hashlib
from functools import wraps
from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for
from db import init_app
import db as database

app = Flask(__name__)
app.secret_key = 'mysecretkey123'
app.permanent_session_lifetime = timedelta(days=30)
init_app(app)


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('you need to login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def calculate_bmr(weight, height, age, gender):
    # mifflin st jeor formula
    base = 10 * weight + 6.25 * height - 5 * age
    return base + 5 if gender == 'male' else base - 161


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return 'welcome ' + session['user_name']


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        height   = float(request.form['height'])
        weight   = float(request.form['weight'])
        age      = int(request.form['age'])
        gender   = request.form['gender']

        db = database.get_db()
        if db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
            flash('this email is already used', 'danger')
            return render_template('auth/register.html')

        bmr = calculate_bmr(weight, height, age, gender)
        db.execute(
            'INSERT INTO users (name, email, password, height, weight, age, gender, calorie_goal) VALUES (?,?,?,?,?,?,?,?)',
            (name, email, hash_pw(password), height, weight, age, gender, bmr)
        )
        db.commit()
        flash('account created you can login now', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        remember = request.form.get('remember')

        db   = database.get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if not user or user['password'] != hash_pw(password):
            flash('wrong email or password', 'danger')
            return render_template('auth/login.html')

        session.clear()
        session['user_id']   = user['id']
        session['user_name'] = user['name']
        if remember:
            session.permanent = True
        return redirect(url_for('index'))
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('you logged out', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        from db import init_db
        init_db()
    app.run(debug=True)
