from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def calculate_gpa(grades, units):
    grade_total=0
    total_credits=0

    for grade in range(len(grades)):
        if grades[grade] >= 70:
            grade_points=4.0
        elif grades[grade] >= 60:
            grade_points=3.0
        elif grades[grade] >= 50:
            grade_points=2.0
        elif grades[grade] >= 40:
            grade_points=1.0
        else:
            grade_points=0.0

        grade_total= grade_total + grade_points * units["grades"]
        total_credits = total_credits + units["grades"]

    Gpa = round(grade_total / total_credits, 2)

    return Gpa