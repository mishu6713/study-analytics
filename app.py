from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    return sqlite3.connect("database.db")


@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()

    user_id = session["user_id"]

    c.execute(
        "SELECT date, minutes FROM study_logs WHERE user_id=?",
        (user_id,)
    )

    data = c.fetchall()

    dates = [row[0] for row in data] if data else []
    minutes = [row[1] for row in data] if data else []

    total = sum(minutes)

    conn.close()

    return render_template(
        "dashboard.html",
        dates=dates,
        minutes=minutes,
        total=total
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()

        c.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect("/")

    return render_template("login.html")


@app.route("/add", methods=["POST"])
def add():

    subject = request.form["subject"]
    minutes = int(request.form["minutes"])

    user_id = session["user_id"]

    today = str(date.today())

    conn = get_db()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO study_logs (user_id,date,subject,minutes)
        VALUES (?,?,?,?)
        """,
        (user_id, today, subject, minutes)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
