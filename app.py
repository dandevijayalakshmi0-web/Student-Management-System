from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Function to initialize database
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName TEXT UNIQUE,
            Password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")


    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                       (name, age, course))
        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("index.html")


@app.route("/view")
def view():
    if "user" not in session:
        return redirect("/Login")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, course FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("view.html", students=students)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/view")

@app.route("/Edit/<int:id>", methods=["GET", "POST"])
def Edit(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        cursor.execute(
            "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
            (name, age, course, id)
        )
        conn.commit()
        conn.close()

        return redirect("/view")

    cursor.execute("SELECT name, age, course FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("Edit.html", student=student)

@app.route("/Register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        UserName = request.form["UserName"]
        Password = request.form["Password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute( "INSERT INTO users (UserName, Password) VALUES (?,?)", (UserName, Password) )
        conn.commit()
        conn.close()

        return redirect("/Login")

    return render_template("Register.html")

@app.route("/Login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        UserName = request.form["UserName"]
        Password = request.form["Password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE UserName=? AND Password=?",
            (UserName, Password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = UserName
            return redirect("/view")
        else:
            return "Invalid Credentials"

    return render_template("Login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/Login")

@app.route("/api/students", methods=["GET"])
def api_get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, course FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3]
        })

    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True)