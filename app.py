from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os
from dotenv import load_dotenv
import secrets
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_cors import CORS
import logging
import sqlite3
from functools import partial
from datetime import datetime
from contextlib import closing


load_dotenv()

app = Flask(__name__,  template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

db = SQLAlchemy(app)
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.remember_cookie_duration = timedelta(days=7)
migrate = Migrate(app, db)
mail = Mail(app)

# Enable debug logging for flask_mail
mail.init_app(app)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

    
"""
Define the User class with columns for user details and quiz results.
"""    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.username}')"

    def generate_reset_token(self):
        """
        Method to generate a reset token for password reset.
        """
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)

    def check_reset_token_valid(self):
        return self.reset_token_expires > datetime.utcnow()

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

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
    quizzes = [
        {'chapter': 1, 'title': 'Chapter 1: Basics'},
        {'chapter': 2, 'title': 'Chapter 2: Advanced Topics'},
        {'chapter': 3, 'title': 'Chapter 3: Intermediate Topics'},
        {'chapter': 4, 'title': 'Chapter 4: Advanced Topics'},
        {'chapter': 5, 'title': 'Chapter 5: Expert Topics'}
    ]
    return render_template('dashboard.html', username=current_user.username, quizzes=quizzes)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
    
# function to retrieve questions based on chapter

def get_questions_for_chapter(chapter):
    questions = {
    1: [
        {
            "id": 0,
            "question": "In Java, how should parentheses be used in mathematical calculations?",
            "choices": [
                "They are optional and can be omitted.",
                "They are required to indicate the order of operations.",
                "They are only used for readability and have no effect.",
                "They should only be used for division operations."
            ],
            "correct_answer": 2
        },
        {
           "id": 1,
            "question": "What happens in Java when both operands in a division are integers?",
            "choices": [
                "The result is always a floating-point number.",
                "The result is rounded to the nearest integer.",
                "The result is an integer, ignoring any decimal part.",
                "The result will cause a compile-time error."
            ],
            "correct_answer": 3
        },
        {
           "id": 2,
            "question": "When encountering a problem with the nextLine() method after reading integers, what causes the issue?",
            "choices": [
                "The method doesn't exist in Java.",
                "The program skips input due to a newline character left in the buffer.",
                "The method cannot read string values.",
                "The method only works with floating-point numbers."
            ],
            "correct_answer": 2
        },
        {
           "id": 3,
            "question": "What is the purpose of the Scanner class in Java?",
            "choices": [
                "To create a graphical user interface for input.",
                "To read input from various sources, including the keyboard.",
                "To compile Java code.",
                "To store data permanently in a file."
            ],
            "correct_answer": 2
        },
        {
            "id": 4,
            "question": "What is the difference between integer division and floating-point division in Java?",
            "choices": [
                "Integer division returns the quotient without any decimal part, while floating-point division can return a decimal result.",
                "Integer division is faster than floating-point division.",
                "Integer division can only be done with positive numbers.",
                "Floating-point division is performed using the modulus operator."
            ],
            "correct_answer": 1
        }
    ],  # Questions for chapter 1
    2: [
        {
            "id": 0,
            "question": "What is the ASCII value for the character 'A'?",
            "choices": [
                "65",
                "97",
                "49",
                "100"
            ],
            "correct_answer": 1
        },
        {
            "id": 1,
            "question": "Which method is used to read a character from a string in Java?",
            "choices": [
                "readChar()",
                "getCharacter()",
                "charAt()",
                "fetchChar()"
            ],
            "correct_answer": 3
        },
        {
            "id": 2,
            "question": "What data type stores values in 2 bytes?",
            "choices": [
                "byte",
                "short",
                "int",
                "double"
            ],
            "correct_answer": 2
        },
        {
            "id": 3,
            "question": "What is the result of Math.round(2.6) in Java?",
            "choices": [
                "2",
                "3",
                "2.6",
                "2.0"
            ],
            "correct_answer": 2
        },
        {
            "id": 4,
            "question": "Which conversion is known as 'widening conversion'?",
            "choices": [
                "byte to int",
                "int to byte",
                "char to byte",
                "double to int"
            ],
            "correct_answer": 1
        }
    ],  # Questions for chapter 2
    3: [
        {
            "id": 0,
            "question": "What does the unary minus operator do?",
            "choices": [
                "Increases the value of a variable by 1",
                "Converts a variable to its positive equivalent",
                "Converts a variable to its negative equivalent",
                "Does nothing"
            ],
            "correct_answer": 3
        },
        {
            "id": 1,
            "question": "What is the purpose of the unary plus operator?",
            "choices": [
                "To decrease the value of a variable by 1",
                "To emphasize numeric promotion from char to int",
                "To make the code less readable",
                "To convert a value to its negative equivalent"
            ],
            "correct_answer": 2
        },
        {
            "id": 2,
            "question": "What is the result of the expression 'int x = 5 * a++' if 'a' initially equals 10?",
            "choices": [
                "x = 50, a = 10",
                "x = 50, a = 11",
                "x = 55, a = 11",
                "x = 55, a = 10"
            ],
            "correct_answer": 2
        },
        {
            "id": 3,
            "question": "Which of the following is an example of a compound assignment operator?",
            "choices": [
                "+=",
                "++",
                "--",
                "!"
            ],
            "correct_answer": 1
        },
        {
            "id": 4,
            "question": "What is the output of the following statements?\nint iValue = 22, iCount = 10;\nString sName = \"Sofia\";\nSystem.out.println (\"Hi\" + \"\\n\"+ sName);\nSystem.out.println (\"Calculate: answer \\t\\\"times\\\" \\t count is:\");\nSystem.out.println (\"\\t\"+iCount*iValue);",
            "choices": [
                "Hi\nSofia\nCalculate: answer \t\"times\" \t count is:\n\t220",
                "HiSofiaCalculate: answer \t\"times\" \t count is:\t220",
                "Hi\\nSofia\\nCalculate: answer \\t\\\"times\\\" \\t count is:\\n\\t220",
                "Hi\nSofiaCalculate: answer \"times\" count is:\n220"
            ],
            "correct_answer": 1
        }
    ],  # Questions for chapter 3
    4: [
        {
            "id": 0,
            "question": "What is the correct order of operations in Java for mathematical expressions?",
            "choices": [
                "Exponents, Parentheses, Multiply Divide MOD, Add Subtract",
                "Parentheses, Exponents, Multiply Divide MOD, Add Subtract",
                "Parentheses, Method calls, Multiply Divide MOD, Add Subtract",
                "Method calls, Parentheses, Multiply Divide MOD, Add Subtract"
            ],
            "correct_answer": 3
        },
        {
            "id": 1,
            "question": "How are exponents and square roots handled in Java according to the provided text?",
            "choices": [
                "Using the Math.exp() and Math.root() methods respectively",
                "Using nested method calls with Math.pow() and Math.sqrt()",
                "Using the ^ operator for exponents and sqrt() for square roots",
                "Using Math.exp() for exponents and ^ for square roots"
            ],
            "correct_answer": 2
        },
        {
            "id": 2,
            "question": "What is the equivalent Java assignment statement for the mathematical equation C = 25?",
            "choices": [
                "int C = sqrt(25);",
                "double C = Math.pow(25, 1/2);",
                "double C = Math.sqrt(25);",
                "int C = Math.sqrt(25);"
            ],
            "correct_answer": 3
        },
        {
            "id": 3,
            "question": "In the expression F = 3^2 + 4, how would you write it in Java according to the provided text?",
            "choices": [
                "double F = 3^2 + 4;",
                "int F = Math.pow(3, 2) + 4;",
                "double F = Math.pow(3, 2) + 4;",
                "double F = pow(3, 2) + 4;"
            ],
            "correct_answer": 3
        },
        {
            "id": 4,
            "question": "What is the correct Java expression for the following pseudo code: E = K % 3 + A + B / C if B and C are integer values?",
            "choices": [
                "double E = K % 3 + A + B / C;",
                "int E = K % 3 + A + B / C;",
                "double E = K % 3 + A + (double) B / C;",
                "int E = K % 3 + A + (int) B / C;"
            ],
            "correct_answer": 3
        }
    ],  # Questions for chapter 4
    5: [
        {
            "id": 0,
            "question": "What will be the output of the following code snippet?\n\nint x = 5;\nx = x + 2 * 3 - 1;\nSystem.out.println(x);",
            "choices": [
                "10",
                "11",
                "12",
                "13"
            ],
            "correct_answer": 1
        },
        {
            "id": 1,
            "question": "Which method is used to convert a string to an integer in Java?",
            "choices": [
                "Integer.parse()",
                "Integer.valueOf()",
                "Integer.parseInt()",
                "String.toInt()"
            ],
            "correct_answer": 3
        },
        {
            "id": 2,
            "question": "What is the value of result after the following code executes?\n\nint result = 3;\nresult *= 4 + 2;",
            "choices": [
                "9",
                "18",
                "12",
                "24"
            ],
            "correct_answer": 2
        },
        {
            "id": 3,
            "question": "What is the output of the following code?\n\nboolean a = true;\nboolean b = false;\nSystem.out.println(a && b);",
            "choices": [
                "true",
                "false",
                "1",
                "0"
            ],
            "correct_answer": 2
        },
        {
            "id": 4,
            "question": "Which of the following is a valid declaration of a float variable in Java?",
            "choices": [
                "float num = 2.5;",
                "float num = 2.5F;",
                "float num = (float) 2.5;",
                "Both B and C"
            ],
            "correct_answer": 4
        },
        {
            "id": 5,
            "question": "What is the output of the following code?\n\nString str = \"Hello, World!\";\nSystem.out.println(str.substring(7, 12));",
            "choices": [
                "World",
                "World!",
                ", Wor",
                "orld"
            ],
            "correct_answer": 1
        },
        {
            "id": 6,
            "question": "Which statement is used to stop the execution of a loop in Java?",
            "choices": [
                "stop",
                "break",
                "exit",
                "return"
            ],
            "correct_answer": 2
        },
        {
            "id": 7,
            "question": "What will be the result of the following code?\n\nint a = 5;\nint b = 2;\ndouble result = a / b;\nSystem.out.println(result);",
            "choices": [
                "2.0",
                "2.5",
                "2",
                "2.00"
            ],
            "correct_answer": 1
        },
        {
            "id": 8,
            "question": "Which keyword is used to define a class in Java?",
            "choices": [
                "define",
                "class",
                "struct",
                "new"
            ],
            "correct_answer": 2
        },
        {
            "id": 9,
            "question": "What is the correct way to create an array of integers in Java?",
            "choices": [
                "int arr[] = new int[5];",
                "int arr[] = {1, 2, 3, 4, 5};",
                "int arr[5];",
                "Both B and C"
            ],
            "correct_answer": 1
        }
    ],  # Questions for chapter 5
}
 # Results dictionary to store results for each chapter
    results = {chapter: [] for chapter in questions.keys()}
    return questions.get(chapter, [])

@app.route("/terms")
def terms():
    return render_template('terms.html')

@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.generate_reset_token()
            db.session.commit()
            send_password_reset_email(user)
            flash('An email with instructions to reset your password has been sent.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email address not found.', 'danger')
    return render_template('forgot_password.html')

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.check_reset_token_valid():
        flash('Invalid or expired token. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        flash('Your password has been reset successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('reset_password.html', token=token)

@app.route("/course")
@login_required
def course():
    return render_template('course.html')
    
def calculate_score(questions, user_answers):
    # Implement logic to compare user answers with correct answers and calculate the score
    score = 0
    for question, answer in questions.items():
        if user_answers[question] == answer['correct_answer']:
            score += 1
    return score


@app.route('/quiz/<int:chapter>', methods=['GET', 'POST'])
@login_required
def quiz(chapter):
    questions = get_questions_for_chapter(chapter)
    if not questions:
        return render_template('404.html')
    if request.method == 'POST':
        form_data = request.form
        data = request.get_json()  # Get the JSON data from the request
        score = 0
        for idx, question in enumerate(questions):
            correct_answer = question['correct_answer']
            if data.get(f'question{idx + 1}') == str(correct_answer):
                score += 1
        # Save the score to the database using SQLAlchemy
        new_result = QuizResult(user_id=current_user.id, score=score)
        db.session.add(new_result)
        db.session.commit()
        return jsonify({'score': score, 'total': len(questions)})
    return render_template('quiz.html', chapter=chapter, questions=questions, enumerate=enumerate)

def save_quiz_result(user_id, score, date):
    DATABASE = 'site.db'
    print(f"Attempting to save quiz result: user_id={user_id}, score={score}, date={date}")
    try:
        with closing(sqlite3.connect(DATABASE)) as connection:
            with closing(connection.cursor()) as cursor:
                # Create table if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS quiz_result (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        score INTEGER NOT NULL,
                        date DATETIME NOT NULL
                    )
                ''')
                print("Table check/creation successful.")
                
                # Insert the quiz result
                cursor.execute('''
                    INSERT INTO quiz_result (user_id, score, date) VALUES (?, ?, ?)
                ''', (user_id, score, date))
                print("Insertion successful.")
                
                connection.commit()
                print("Commit successful.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e.args[0]}")
        raise
    except Exception as e:
        print(f"Error saving quiz result: {e}")
        raise

from datetime import datetime

@app.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    try:
        data = request.get_json()
        score = data.get('chapterScore')
        date_str = data.get('date')

        # Remove the 'Z' if it exists
        if date_str.endswith('Z'):
            date_str = date_str[:-1]
        
        # Convert the string to a datetime object
        date = datetime.fromisoformat(date_str)

        user_id = current_user.id  # Get the user_id from current_user
        print(f"Parsed Data - user_id: {user_id}, score: {score}, date: {date}")

        # Save the quiz result to the database
        new_result = QuizResult(user_id=user_id, score=score, date=date)
        db.session.add(new_result)
        db.session.commit()
        return jsonify({"message": "Quiz result saved successfully"}), 200
    except Exception as e:
        print(f"Error in submit_quiz: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


    
@app.route("/profile")
@login_required
def profile():
    # Fetch the user's quiz results
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.date.desc()).all()
    return render_template('profile.html', quiz_results=quiz_results)
    
def send_password_reset_email(user):
    token = user.reset_token
    msg = Message('Password Reset Request',
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)

 
if __name__ == "__main__":
     app.run(debug=True)
 