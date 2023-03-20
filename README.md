# Student_Management_System

<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>
<!-- https://user-images.githubusercontent.com/100721103/200149633-373db975-c47f-43a7-9288-f6cbd16e0410.mp4 -->
<br><br>
<!-- Project Shields -->
<div align="center">
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]
[//]: # ([![Twitter][twitter-shield2]][twitter-url2])
</div>
<br />
<div>
  <p align="center">
    <a href="https://github.com/Olajiive/Student_Management_System#readme"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/Olajiive/Student_Management_System/issues">Report Bug</a>
    ·
    <a href="https://github.com/Olajiive/Student_Management_System/issues">Request Feature</a>
  </p>
</div>
---
<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-">About the project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
      <li><a href="#demo">Demo</a></li>
    </li>
    <li>
      <a href="#exposure">Exposure</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
         <li><a href="#endpoints">Endpoints</a></li>
      </ul>
    <!-- <li><a href="#shots">Shots</a></li> -->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>
---
<!-- About the api -->
## About
This is a Student management system's API. It is a RESTful API that allows students to register for courses and admins to manage courses and students.
### Features
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
<p align="right"><a href="#readme-top">back to top</a></p>
### Built With:
![Python][python]
![Flask][flask]
![SQLite][sqlite]
<p align="right"><a href="#readme-top">back to top</a></p>
---
<br>
<p align="right"><a href="#readme-top">back to top</a></p>

<br><p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
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
<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- GETTING STARTED -->
## Usage
To get a local copy up and running, follow the steps below.
### Prerequisites
Python3: [Get Python](https://www.python.org/downloads/)
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
   <br>
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
   ├── requirements.txt
   └── runserver.py
   ```  
### Endpoints
<br>
POST (Register) http://127.0.0.1:5000/register
REQUEST
```json
{
  "first_name": "string",
  "password": "string",
  "email": "string@string.com",
  "last_name": "string"
}
```
RESPONSE
```json
{
    "id": 1,
    "first_name": "string",
    "password": "string",
    "email": "string@string.com",
    "last_name": "string"
}
```
POST (Login) http://127.0.0.1:5000/login
REQUEST
```json
{
  "user_id": "USER_ID",
  "password": "string"
}
```
RESPONSE
```json
  {
    "access_token": "eyJhbGciOiJIUzIEyMjMtNj...................",
    "refresh_token": "eyJhbGciOiJIUzLyADmyXA...................."
  }
```
POST (Create Student) http://127.0.0.1:5000/create-student <br>
@admin_required
REQUEST
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}
```
RESPONSE
```json
```json
  {
    "stud_id": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string"
  }
```
POST (Create course) http://127.0.0.1:5000/create-course <br>
@admin_required
REQUEST
```json
{
  "teacher": "string",
  "course_title": "string",
  "course_code": "string",
  "course_unit": 0
}
```
GET (Get all students) http://127.0.0.1:5000/students <br>
@admin_required
RESPONSE
```json
[
  {
    "stud_id": "string",
    "id": 0,
    "first_name": "string",
    "email": "string",
    "gpa": 0,
    "registered_courses": {
      "id": 0,
      "course_title": "string",
      "grade": 0,
      "course_code": "string",
      "course_unit": 0
    },
    "last_name": "string"
  }
]
```
GET (Get all courses with registered students) http://127.0.0.1:5000/courses-students <br>
@admin_required
RESPONSE
```json
[
  {
    "id": 0,
    "created_at": "2023-03-14T01:59:20.927Z",
    "teacher": "string",
    "course_title": "string",
    "year": 0,
    "course_code": "string",
    "course_unit": 0,
    "student_registered": {
      "stud_id": "string",
      "first_name": "string",
      "last_name": "string",
      "grade": 0
    }
  }
]

```
GET (Get specific student) http://127.0.0.1:5000/student/<stud_id> <br>
@admin_required
RESPONSE
```json
{
  "stud_id": "string",
  "id": 0,
  "first_name": "string",
  "email": "string",
  "gpa": 0,
  "registered_courses": {
    "id": 0,
    "course_title": "string",
    "grade": 0,
    "course_code": "string",
    "course_unit": 0
  },
  "last_name": "string"
}
```
<p align="right"><a href="#readme-top">back to top</a></p>
---

[//]: # (<br/>)
[//]: # (<p align="right"><a href="#readme-top">back to top</a></p>)
<!-- Contact -->
## Contact
Olatunji Olasunkanmi - [@jiive_SZN](https://twitter.com/jiive_SZN) - muizolatunji29@gmail.com <br>

Project Link: [student_Management_Api](https://github.com/Olajiive/Student_Management_System)
<p align="right"><a href="#readme-top">back to top</a></p>
---
<!-- Acknowledgements -->
## Acknowledgements
This project was made possible by:
- [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
- [Othneil Drew's README Template](https://github.com/othneildrew/Best-README-Template)
<p align="right"><a href="#readme-top">back to top</a></p>
---
<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/Olajiive/Student_Management_System.svg?style=for-the-badge
[contributors-url]: https://github.com/Olajiive/Student_Management_System/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Olajiive/Student_Management_System.svg?style=for-the-badge
[forks-url]: https://github.com/Olajiive/Student_Management_System/network/members
[stars-shield]: https://img.shields.io/github/stars/Olajiive/Student_Management_System.svg?style=for-the-badge
[stars-url]: https://github.com/Olajiive/Student_Management_System/stargazers
[issues-shield]: https://img.shields.io/github/issues/Olajiive/Student_Management_System.svg?style=for-the-badge
[issues-url]: https://github.com/Olajiive/Student_Management_Systemissues
[license-shield]: https://img.shields.io/github/license/Olajiive/Student_Management_System.svg?style=for-the-badge
[license-url]: https://github.com/Olajiive/Student_Management_System/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@jiive_SZN-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/jiive_SZN
[twitter-url]: https://twitter.com/jiive_SZN

 
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[jinja]: https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black
[html5]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[css3]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[javascript]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[bootstrap]: https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white