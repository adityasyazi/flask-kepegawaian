import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "rahasia"

# =====================
# DATABASE
# =====================
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=3306
    )

# =====================
# UPLOAD CONFIG
# =====================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =====================
# ROUTE TEST (WAJIB ADA)
# =====================
@app.route("/test")
def test():
    return "FLASK HIDUP DI RAILWAY"

# =====================
# ROUTE LOGIN
# =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["login"] = True
            return redirect("/dashboard")
        return "Login gagal"
    return "HALAMAN LOGIN"

# =====================
# ROUTE DASHBOARD
# =====================
@app.route("/dashboard")
def dashboard():
    if not session.get("login"):
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT NIP, Nama, foto FROM pegawai")
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return data
