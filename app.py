from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(5), nullable=False)

with app.app_context():
        db.create_all()

# Home route — ✅ Fetch data from DB
@app.route("/")
def home():
    students = Student.query.all()  # <-- fetch from DB
    return render_template("index.html", students=students, active_page="home")

@app.route("/about/")
def about():
    return render_template("about.html", active_page="about")

@app.route("/contact/")
def contact():
    return render_template("contact.html", active_page="contact")

@app.route("/branch/")
def branch():
    return render_template("branch.html", active_page="branch")

# Add new student — ✅ Save to DB
@app.route("/add/", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        roll = request.form.get("roll")
        student_class = request.form.get("class")
        subject = request.form.get("subject")
        grade = request.form.get("grade")

        new_student = Student(
            name=name,
            roll=roll,
            student_class=student_class,
            subject=subject,
            grade=grade
        )
        db.session.add(new_student)
        db.session.commit()  # save changes

        return redirect(url_for("home"))
    return render_template("add_student.html", active_page="add")

# Delete student — ✅ Works with DB
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("home"))

# Update student — ✅ Works with DB
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        student.name = request.form.get("name")
        student.roll = request.form.get("roll")
        student.student_class = request.form.get("class")
        student.subject = request.form.get("subject")
        student.grade = request.form.get("grade")
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_student.html", student=student)

if __name__ == "__main__":
    
    app.run(debug=True)
