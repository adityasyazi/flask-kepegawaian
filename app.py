import os
import mysql.connector
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "rahasia"

# =====================
# DATABASE (RAILWAY)
# =====================
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT", 3306))
    )

# =====================
# TEST ROUTE (WAJIB)
# =====================
@app.route("/")
def home():
    return "FLASK HIDUP DI RAILWAY 🚀"

@app.route("/test")
def test():
    return "TEST OK"

# =====================
# DASHBOARD TEST DB
# =====================
@app.route("/db-test")
def db_test():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        db.close()
        return "KONEKSI DATABASE OK ✅"
    except Exception as e:
        return f"DB ERROR ❌ : {e}"

# =====================
# JANGAN PAKE app.run()
# =====================
