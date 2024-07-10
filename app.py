from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import os
from flask_bcrypt import Bcrypt
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.remember_cookie_duration = timedelta(days=7)  # Optional: set duration for remember me
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('vernonbaloyi41@gmail.com')  # replace with your email
app.config['MAIL_PASSWORD'] = os.environ.get('wgyd qera uolp ssqt')  # replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('vernonbaloyi41@gmail.com')  # ensure this matches the authenticated email


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.username}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            remember = 'remember' in request.form
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=remember)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('The email or password that you\'ve entered is incorrect. Please try again.', 'danger')
        elif 'register' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hello, {current_user.username}!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route("/terms")
def terms():
    return render_template('terms.html')

@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            msg = Message('Your QuizMaster Password',
                          sender='noreply@demo.com',
                          recipients=[email])
            msg.body = f'Your password is: {user.password}'
            mail.send(msg)
            flash('An email with your password has been sent!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email address not found', 'danger')
    return render_template('forgot_password.html')



if __name__ == '__main__':
    app.run(debug=True)
