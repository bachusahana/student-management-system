
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

print("ENV FILE:", env_path)
print("ENV EXISTS:", env_path.exists())
print("DB HOST LOADED:", bool(os.getenv("DB_HOST")))
print("DB USER LOADED:", bool(os.getenv("DB_USER")))
print("DB PASSWORD LOADED:", bool(os.getenv("DB_PASSWORD")))
print("DB NAME LOADED:", bool(os.getenv("DB_NAME")))

# Load the exact .env file inside backend
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


@app.route("/add_student", methods=["POST"])
def add_student():
    full_name = request.form["full_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]
    gender = request.form["gender"]

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO students
            (full_name, email, phone, course, gender)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (full_name, email, phone, course, gender)

        cursor.execute(query, values)
        connection.commit()

        flash("Student added successfully!", "success")

    except mysql.connector.IntegrityError:
        connection.rollback()
        flash("Email already exists!", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))

@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if request.method == "POST":
            full_name = request.form["full_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            course = request.form["course"]
            gender = request.form["gender"]

            query = """
                UPDATE students
                SET full_name=%s, email=%s, phone=%s,
                    course=%s, gender=%s
                WHERE id=%s
            """

            values = (
                full_name, email, phone,
                course, gender, student_id
            )

            cursor.execute(query, values)
            connection.commit()

            flash("Student updated successfully!", "success")
            return redirect(url_for("index"))

        cursor.execute(
            "SELECT * FROM students WHERE id=%s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            flash("Student not found!", "error")
            return redirect(url_for("index"))

        return render_template("edit_student.html", student=student)

    except mysql.connector.IntegrityError:
        connection.rollback()
        flash("Email already exists!", "error")
        return redirect(url_for("edit_student", student_id=student_id))

    finally:
        cursor.close()
        connection.close()


@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM students WHERE id=%s",
            (student_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            flash("Student deleted successfully!", "success")
        else:
            flash("Student not found!", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
    
print("ENV FILE FOUND:", env_path.exists())
print("DB HOST:", bool(os.getenv("DB_HOST")))
print("DB USER:", bool(os.getenv("DB_USER")))
print("DB PASSWORD:", bool(os.getenv("DB_PASSWORD")))
print("DB NAME:", bool(os.getenv("DB_NAME")))