from flask import Flask, render_template_string, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "jayson-secret-key"

STYLE = """
<style>
body { font-family: Arial, sans-serif; background-color: #0F1115; color: #ECEFF4; max-width: 600px; margin: 40px auto; padding: 0 20px; }
h1 { color: #58E0C9; }
a { color: #58E0C9; }
</style>
"""

SUBJECTS_PAGE = """
<!DOCTYPE html><html><head><title>Subjects</title>""" + STYLE + """</head>
<body>
<h1>Science Stream Subjects</h1>
<ul>
{% for subject in subjects %}
<li><a href="/subject/{{ subject }}">{{ subject }}</a></li>
{% endfor %}
</ul>
</body></html>
"""

SUBJECT_PAGE = """
<!DOCTYPE html><html><head><title>{{ name }}</title>""" + STYLE + """</head>
<body>
<h1>{{ name }}</h1>
{% if name == "Physics" %}
<p>Motion means a change in position over time. Speed is calculated as distance divided by time: v = s / t.</p>
<h2>Quick Quiz</h2>
<form action="/subject/Physics/quiz" method="POST">
<p>A car travels 100 km in 2 hours. What is its speed?</p>
<input type="radio" name="answer" value="a"> 25 km/h<br>
<input type="radio" name="answer" value="b"> 50 km/h<br>
<input type="radio" name="answer" value="c"> 100 km/h<br>
<button type="submit">Submit</button>
</form>
{% else %}
<p>Welcome to the {{ name }} subject page.</p>
{% endif %}
<a href="/">Back to subjects</a>
</body></html>
"""

QUIZ_RESULT_PAGE = """
<!DOCTYPE html><html><head><title>Quiz Result</title>""" + STYLE + """</head>
<body>
<h1>Quiz Result</h1>
<p>{{ result }}</p>
<a href="/subject/Physics">Back to Physics</a>
</body></html>
"""

SIGNUP_PAGE = """
<!DOCTYPE html><html><head><title>Sign Up</title>""" + STYLE + """</head>
<body>
<h1>Create Your Account</h1>
<form action="/signup" method="POST">
<p>Username: <input type="text" name="username"></p>
<p>Password: <input type="password" name="password"></p>
<button type="submit">Sign Up</button>
</form>
<a href="/login">Already have an account? Log in</a>
</body></html>
"""

LOGIN_PAGE = """
<!DOCTYPE html><html><head><title>Log In</title>""" + STYLE + """</head>
<body>
<h1>Log In</h1>
<form action="/login" method="POST">
<p>Username: <input type="text" name="username"></p>
<p>Password: <input type="password" name="password"></p>
<button type="submit">Log In</button>
</form>
{% if error %}
<p style="color: red;">{{ error }}</p>
{% endif %}
<a href="/signup">New here? Sign up</a>
</body></html>
"""

def get_db():
    conn = sqlite3.connect("eduverse.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    return conn

@app.route("/")
def home():
    subjects = ["English", "Mathematics", "Physics", "Chemistry", "Biology"]
    return render_template_string(SUBJECTS_PAGE, subjects=subjects)

@app.route("/subject/<name>")
def subject(name):
    return render_template_string(SUBJECT_PAGE, name=name)

@app.route("/subject/Physics/quiz", methods=["POST"])
def physics_quiz():
    answer = request.form.get("answer")
    if answer == "b":
        result = "Correct! 100 km ÷ 2 h = 50 km/h"
    else:
        result = "Not quite. The correct answer is 50 km/h (100 km ÷ 2 h)."
    return render_template_string(QUIZ_RESULT_PAGE, result=result)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        session["username"] = username
        return redirect("/")
    return render_template_string(SIGNUP_PAGE)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db()
        row = conn.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if row and row[0] == password:
            session["username"] = username
            return redirect("/")
        return render_template_string(LOGIN_PAGE, error="Wrong username or password")
    return render_template_string(LOGIN_PAGE)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
