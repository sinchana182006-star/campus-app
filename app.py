from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ------------------ DATABASE ------------------
def init_db():
    conn = sqlite3.connect("data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        )
    """)
    conn.close()

init_db()

# ------------------ LOGIN ------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if username == "admin" and password == "admin" and role == "admin":
            return redirect("/admin")

        elif username == "student" and password == "student" and role == "student":
            return redirect("/student")

        else:
            return "Invalid Login ❌"

    return render_template("login.html")

# ------------------ ADMIN ------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    conn = sqlite3.connect("data.db")

    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]

        conn.execute("INSERT INTO notice (title, description) VALUES (?, ?)", (title, desc))
        conn.commit()

    data = conn.execute("SELECT * FROM notice ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("admin.html", data=data)

# ------------------ DELETE ------------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("data.db")
    conn.execute("DELETE FROM notice WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ------------------ STUDENT ------------------
@app.route("/student")
def student():
    conn = sqlite3.connect("data.db")
    data = conn.execute("SELECT * FROM notice ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("student.html", data=data)

# ------------------
if __name__ == "__main__":
    app.run(debug=True)