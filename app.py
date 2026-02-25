from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename 


# -----------------------------------------------------
# USE ONLY ONE DATABASE
# -----------------------------------------------------
DATABASE = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.secret_key = "mysecretkey123"

# -----------------------------------------------------
# FILE UPLOAD SETUP
# -----------------------------------------------------
UPLOAD_FOLDER = "static/profile_pics"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------------------------------
# CREATE USERS TABLE
# -----------------------------------------------------
def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT,
            profile_pic TEXT
        )
    """)
    conn.commit()
    conn.close()

create_database()


# -----------------------------------------------------
# HOME
# -----------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------------------------------
# PROBLEM PAGE (FIXED VERSION)
# -----------------------------------------------------
@app.route("/problem/<int:problem_id>")
def problem_page(problem_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    problem = conn.execute(
        "SELECT * FROM problems WHERE id = ?", (problem_id,)
    ).fetchone()

    conn.close()

    if not problem:
        return "Problem not found", 404

    return render_template(
        "problem_page.html",
        problem=problem,
        username=session.get("username"),
        profile_pic=session.get("profile_pic")
    )


@app.route("/solve/<int:problem_id>", methods=["GET", "POST"])
def solve_problem(problem_id):

    # Fetch problem details
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    problem = conn.execute(
        "SELECT * FROM problems WHERE id = ?", (problem_id,)
    ).fetchone()
    conn.close()

    if not problem:
        return "Problem not found", 404

    output = ""
    user_code = ""

    if request.method == "POST":
        user_code = request.form["code"]

        try:
            # SAFELY execute code
            local_vars = {}
            exec(user_code, {}, local_vars)
            output = str(local_vars.get("output", "No output variable returned"))
        except Exception as e:
            output = str(e)

    return render_template(
        "solve_page.html",
        problem=problem,
        code=user_code,
        output=output
    )



# -----------------------------------------------------
# LOGIN
# -----------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", 
                            (email, password)).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]
            session["username"] = user["username"]
            session["profile_pic"] = user["profile_pic"]
            return redirect("/dashboard")
        else:
            flash("Invalid email or password!", "error")
            return redirect("/login")

    return render_template("login.html")


# -----------------------------------------------------
# REGISTER
# -----------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO users (fullname, username, email, password, profile_pic)
                VALUES (?, ?, ?, ?, ?)
            """, (fullname, username, email, password, None))
            conn.commit()
            conn.close()
            return redirect("/register?success=1")

        except:
            flash("Email already exists!", "error")
            return redirect("/register")

    return render_template("register.html")


# -----------------------------------------------------
# DASHBOARD
# -----------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT username, profile_pic FROM users WHERE id=?", (session["user_id"],))
    user = c.fetchone()
    conn.close()

    session["username"] = user["username"]
    session["profile_pic"] = user["profile_pic"]

    return render_template(
        "dashboard.html",
        username=user["username"],
        profile_pic=user["profile_pic"]
    )


# -----------------------------------------------------
# STAGES PAGE
# -----------------------------------------------------
@app.route("/stages")
def stages():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "stages.html",
        username=session.get("username"),
        profile_pic=session.get("profile_pic")
    )


# -----------------------------------------------------
# SINGLE STAGE PAGE (unchanged)
# -----------------------------------------------------
@app.route("/stage/<int:number>")
def stage_page(number):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    problems = conn.execute(
        "SELECT * FROM problems WHERE stage = ?", (number,)
    ).fetchall()
    conn.close()

    return render_template(
        "stage_page.html",
        stage_number=number,
        problems=problems,
        username=session.get("username"),
        profile_pic=session.get("profile_pic")
    )


# -----------------------------------------------------
# PROFILE PAGE
# -----------------------------------------------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id=?", (session["user_id"],)
    ).fetchone()
    conn.close()

    session["profile_pic"] = user["profile_pic"]

    return render_template(
        "profile.html",
        fullname=user["fullname"],
        username=user["username"],
        email=user["email"],
        profile_pic=user["profile_pic"]
    )


# -----------------------------------------------------
# EDIT PROFILE
# -----------------------------------------------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        if old_password != user["password"]:
            flash("Old password incorrect!", "error")
            return redirect("/edit-profile")

        final_password = new_password if new_password else user["password"]

        file = request.files.get("profile_pic")
        profile_pic_name = user["profile_pic"]

        if file and file.filename != "":
            if allowed_file(file.filename):
                ext = file.filename.rsplit(".", 1)[1].lower()
                filename = f"user_{session['user_id']}.{ext}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                profile_pic_name = filename
            else:
                flash("Only PNG / JPG / JPEG allowed!", "error")
                return redirect("/edit-profile")

        conn.execute("""
            UPDATE users SET fullname=?, username=?, email=?, password=?, profile_pic=?
            WHERE id=?
        """, (fullname, username, email, final_password, profile_pic_name, session["user_id"]))
        conn.commit()
        conn.close()

        session["username"] = username
        session["profile_pic"] = profile_pic_name

        flash("Profile updated!", "success")
        return redirect("/profile")

    conn.close()

    return render_template(
        "edit_profile.html",
        fullname=user["fullname"],
        username=user["username"],
        email=user["email"],
        profile_pic=user["profile_pic"]
    )

@app.route("/run_code", methods=["POST"])
def run_code():
    import subprocess, tempfile
    from flask import jsonify

    code = request.json["code"]

    # Create temp python file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        f.flush()

        try:
            output = subprocess.check_output(
                ["python", f.name],
                stderr=subprocess.STDOUT,
                timeout=5
            ).decode()
        except subprocess.CalledProcessError as e:
            output = e.output.decode()
        except subprocess.TimeoutExpired:
            output = "Error: Timed Out"

    return jsonify({"output": output})


# -----------------------------------------------------
# LOGOUT
# -----------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------------------------------
# RUN APP
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)