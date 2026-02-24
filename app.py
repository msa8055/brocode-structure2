from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# ---------------- FILE UPLOAD SETTINGS ----------------
UPLOAD_FOLDER = "static/profile_pics"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- DATABASE SETUP ----------------
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


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[2]
            session["profile_pic"] = user[5]   # STORE PROFILE PIC IN SESSION
            return redirect("/dashboard")
        else:
            flash("Invalid email or password!", "error")
            return redirect("/login")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("""
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


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT fullname, username, email, profile_pic FROM users WHERE id=?", 
              (session["user_id"],))
    user = c.fetchone()
    conn.close()

    return render_template(
        "profile.html",
        fullname=user[0],
        username=user[1],
        email=user[2],
        profile_pic=user[3]
    )


# ---------------- EDIT PROFILE ----------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (session["user_id"],))
    user = c.fetchone()

    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        # ---------------- CHECK OLD PASSWORD ----------------
        if old_password != user[4]:
            flash("Old password is incorrect!", "error")
            return redirect("/edit-profile")

        final_password = new_password if new_password else user[4]

        # ---------------- HANDLE PROFILE PIC ----------------
        file = request.files.get("profile_pic")
        profile_pic_name = user[5]  # keep old if not replaced

        if file and file.filename != "":
            if allowed_file(file.filename):
                ext = file.filename.rsplit(".", 1)[1].lower()
                filename = f"user_{session['user_id']}.{ext}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                profile_pic_name = filename
            else:
                flash("Only PNG, JPG, JPEG allowed!", "error")
                return redirect("/edit-profile")

        # ---------------- UPDATE DATABASE ----------------
        c.execute("""
            UPDATE users 
            SET fullname=?, username=?, email=?, password=?, profile_pic=?
            WHERE id=?
        """, (fullname, username, email, final_password, profile_pic_name, session["user_id"]))

        conn.commit()
        conn.close()

        # ---------------- UPDATE SESSION ----------------
        session["username"] = username
        session["profile_pic"] = profile_pic_name

        flash("Profile updated successfully!", "success")
        return redirect("/profile")

    conn.close()

    return render_template(
        "edit_profile.html",
        fullname=user[1],
        username=user[2],
        email=user[3],
        profile_pic=user[5]
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)