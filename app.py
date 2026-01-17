import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, send_from_directory
from werkzeug.utils import secure_filename

# =====================
# INIT APP
# =====================
app = Flask(__name__)
app.secret_key = "rahasia"

# =====================
# DATABASE LOKAL
# =====================
# db = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="kepegawaian"
# )

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=3306
)

# =====================
# UPLOAD CONFIG
# =====================
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =====================
# ROUTE: UPLOADS
# =====================
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# =====================
# ROUTE: LOGIN
# =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["login"] = True
            return redirect("/dashboard")
        return render_template("login.html", error="Login gagal")
    return render_template("login.html")

# =====================
# ROUTE: DASHBOARD
# =====================
@app.route("/dashboard")
def dashboard():
    if not session.get("login"):
        return redirect("/")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT NIP, Nama, foto FROM pegawai")
    data = cursor.fetchall()
    cursor.close()

    return render_template("dashboard.html", data=data)

# =====================
# ROUTE: TAMBAH
# =====================
@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        nip = request.form.get("NIP")
        nama = request.form.get("Nama")
        foto = request.files.get("foto")

        if not nip or not nama:
            return "NIP dan Nama wajib diisi", 400

        filename = None
        if foto and foto.filename != "":
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        cursor = db.cursor()
        sql = "INSERT INTO pegawai (NIP, Nama, foto) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nip, nama, filename))
        db.commit()
        cursor.close()

        return redirect("/dashboard")

    return render_template("tambah.html")

# =====================
# RUN APP
# =====================
# if __name__ == "__main__":
#    app.run(debug=True)
