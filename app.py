import hashlib
from flask import Flask, flash, redirect, render_template, request, session, url_for
from db import init_app
import db as database

app = Flask(__name__)
app.secret_key = 'mysecretkey123'
init_app(app)


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def calculate_bmr(weight, height, age, gender):
    # mifflin st jeor formula
    base = 10 * weight + 6.25 * height - 5 * age
    return base + 5 if gender == 'male' else base - 161


@app.route('/')
def index():
    return 'hello this is dailyfuel'


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

        print('register attempt:', email)  # debug

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


@app.route('/login')
def login():
    return 'login page coming soon'


if __name__ == '__main__':
    with app.app_context():
        from db import init_db
        init_db()
    app.run(debug=True)
