# A Simple School Management System API Built with Flask, Flask_RestX
---
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Project-Structure](#project structure)
- [Contributing](#contributing)
- [Live Demo](#live-demo)
- [Upcoming Features](#upcoming-features)
- [Exposure](#exposure)
- [Contact](#contact)
- [Acknowledegement](#acknowledgement)
- [License](#license)



## Introduction
This is a simple school management system API built with Flask and Flask_RestX built by according to [this requirements](https://docs.google.com/document/d/19ayXN5P1oV2aqW_7-As6EUpn7OQShkpAlZK4wRbrgBQ/). It is a simple API that allows you if you are an Admin to perform CRUD operations on students and courses. It also allows you to register students to courses and add grade for students.

## Features
- Admins can create, read, update and delete students and courses
- Students get their unique student ID by using their email to fetch it through the right endpoint
- Students can login with their student ID and default password
- Students can register for courses
- Students can view their profiles and courses registered
- Students can change their passwords once, subsequent changes will require the student to contact the admin
- Admins can view all students and courses
- Admins can view all students registered for a course
- Admins can view all courses a student registered for
- Admins can update student's details such as the names and email
- Admins can upload student's grade for each course
- Admins can upload student's GPA

### Installation
1. Clone this repo
   ```sh
   git clone https://github.com/Olajiive/System_Management_System.git
   ```
2. Navigate into the directory
   ```sh
   cd System_Management_System
   ```
3. Create a virtual environment
   ```sh
   python -m venv your_venv_name
   ```
4. Activate the virtual environment on powershell or cmd
   ```sh
   your_venv_name\Scripts\activate.bat
   ```
   On Bash ('Scripts' for windows, 'bin' for linux)
   ```sh
   source your_venv_name/Scripts/activate.csh
   ```
5. Install project dependencies
   ```sh
   pip install -r requirements.txt
   ```
6. Set environment variables
   ```sh
   set FLASK_APP=run.py
   ```
   On Bash
   ```sh
   export FLASK_APP=run.py
   ```
7. Create database
   ```sh
   flask shell
   ```
   ```sh
   >>> Course (hit enter)
   >>> Student (hit enter)
   >>> Admin (hit enter)
   >>> CourseRegistered (hit enter)
   >>> db (hit enter)
   >>> db.create_all()
   >>> exit()
    ```
 
8. Run Flask
   ```sh
   flask run
   ```
   or
   ```sh
   python run.py
   ```
9. Use the link generated on the terminal to access the endpoints
    ```sh
   http://127.0.0.1:5000
   ```
   To use swagger-ui, use the link below
   ```sh
    http://127.0.0.1:5000/swagger-ui
   ```

### Project structure
   ```
   .
   ├── README.md
   ├── .gitignore
   ├── LICENSE
   ├── Api
   │   ├── __init__.py
   │   ├── auth
   │   │   ├── __init__.py
   │   │  
   │   └── config
   │   │   ├── __init__.py
   │   │   ├── db.sqlite3
   │   └── extensions
   │   │   ├── __init__.py
   │   └── models
   │   │   ├── __init__.py
   │   │   ├── admin.py
   │   │   ├── course_registered.py
   │   │   ├── courses.py
   │   │   ├── students.py
   │   └── resources
   │   │   ├── __init__.py
   │   │   ├── admin.py
   │   │   ├── student.py
   │   └── test
   │   │   ├── __init__.py
   │   │   ├── test_course.py
   │   │   ├── test_student_profile.py
   │   │   ├── test_students_by_admin.py
   │   │   ├── test_user.py
   │   └── utils
   │   │   ├── __init__.py
   |   |__ code_gen.py
   |   |__blocklist.py
   |   |__ 
   ├── env
   |__ runtime.txt
   |__ Procfile
   ├── requirements.txt
   └── runserver.py
   ```  

## Contributing
- Fork the repository
- Clone the repository
- Create a virtual environment `python3 -m venv venv` or with `virtualenv venv`
- Install the requirements `pip install -r requirements.txt`
- Create a new branch `git checkout -b new-branch`
- Make your changes
- Commit your changes `git commit -m "commit message"`
- Push to the branch `git push origin new-branch`
- Create a pull request

## Live Demo
- [PythonAnywhere](https://olajiive.pythonanywhere.com//)

## Upcoming Features
- Add more tests / Improve tests (some tests are failing)
- Add more features to the API
- Add more documentation to the API
- Add more features to the Admin dashboard
- Update to Postgres database instead of SQLite for production

## Exposure
Creating this project got me more exposed to:
- Debugging
- Restful API
- Thorough research
- Database Management
- Authentication
- Authorization
- Endpoint restriction
- Testing with unittest
- Testing with Insomnia
- Swagger UI
- API Documentation

## Contact
Olatunji Olasunkanmi - [@jiive_SZN](https://twitter.com/jiive_SZN) - muizolatunji29@gmail.com <br>

Project Link: [student_Management_Api](https://github.com/Olajiive/Student_Management_System)

## Acknowledgements
This project was made possible by:
- [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
- Caleb Emelike

## License
[MIT](https://github.com/Olajiive/Student_Management_System/main/LICENCE)




