from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "medicine_secret_key"
def create_user_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

create_user_table()



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
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

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["username"] = username
            return redirect("/home")

        else:
            return "Invalid Username or Password"

    return render_template("login.html")
@app.route("/")
def start():
    return redirect("/register")
@app.route("/home")
def home():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicine")

    medicines = cursor.fetchall()

    total = len(medicines)
    taken = sum(1 for medicine in medicines if medicine[4] == "Taken")
    pending = total - taken

    conn.close()

    return render_template(
        "index.html",
        medicines=medicines,
        total=total,
        taken=taken,
        pending=pending
    )
@app.route("/add", methods=["POST"])
def add():
    name = request.form["medicine_name"]
    date = request.form["medicine_date"]
    time = request.form["medicine_time"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO medicine (medicine_name, medicine_date, medicine_time, status) VALUES (?, ?, ?, ?)",
    (name, date, time, "Pending")
)
    conn.commit()
    conn.close()

    return redirect("/home")
@app.route("/delete/<int:id>")
def delete(id):
     conn = sqlite3.connect("database.db")
     cursor = conn.cursor()
     cursor.execute("DELETE FROM medicine WHERE id=?", (id,))
     conn.commit()
     conn.close()
     return redirect("/home")
@app.route("/taken/<int:id>")
def taken(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE medicine SET status='Taken' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/home")
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")
   

if __name__ == "__main__":
    app.run(debug=True)
    
   