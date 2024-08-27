import sqlite3
import pandas as pd
from fpdf import FPDF

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('university_results2.db')
cursor = conn.cursor()

# Create tables with autoincrement IDs
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    date_of_birth DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    course_code TEXT UNIQUE NOT NULL,
    credits INTEGER NOT NULL,
    department TEXT,
    professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES Professors(professor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Professors (
    professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    department TEXT,
    phone TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    student_id INTEGER,
    grade TEXT,
    grade_date DATE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    UNIQUE (course_id, student_id)
)    
''')



cursor.execute('''
CREATE TABLE IF NOT EXISTS Course_Requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    request_date DATE,
    status TEXT,
    professor_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (professor_id) REFERENCES Professors(professor_id)
)
''')

# Insert sample data into Professors
professors = [
    ('Dr. John Smith', 'john.smith@university.edu', 'Computer Science', '555-1234'),
    ('Dr. Alice Johnson', 'alice.johnson@university.edu', 'Mathematics', '555-5678'),
    ('Dr. Robert Brown', 'robert.brown@university.edu', 'Physics', '555-9101'),
    ('Dr. Emma Davis', 'emma.davis@university.edu', 'Biology', '555-1122'),
    ('Dr. Olivia Wilson', 'olivia.wilson@university.edu', 'Chemistry', '555-3344'),
    ('Dr. William Taylor', 'william.taylor@university.edu', 'History', '555-5566'),
    ('Dr. Sophia Anderson', 'sophia.anderson@university.edu', 'Economics', '555-7788'),
    ('Dr. James Thomas', 'james.thomas@university.edu', 'Political Science', '555-9900')
]
cursor.executemany('''
INSERT OR IGNORE INTO Professors (name, email, department, phone)
VALUES (?, ?, ?, ?)
''', professors)

# Insert sample data into Courses
courses = [
    ('Introduction to Programming', 'CS101', 3, 'Computer Science', 1),
    ('Data Structures', 'CS102', 4, 'Computer Science', 1),
    ('Calculus I', 'MATH101', 3, 'Mathematics', 2),
    ('Linear Algebra', 'MATH102', 3, 'Mathematics', 2),
    ('Physics I', 'PHYS101', 4, 'Physics', 3),
    ('Biology 101', 'BIOL101', 3, 'Biology', 4),
    ('Organic Chemistry', 'CHEM101', 4, 'Chemistry', 5),
    ('World History', 'HIST101', 3, 'History', 6),
    ('Microeconomics', 'ECON101', 3, 'Economics', 7),
    ('Introduction to Political Science', 'POLI101', 3, 'Political Science', 8)
]
cursor.executemany('''
INSERT OR IGNORE INTO Courses (course_name, course_code, credits, department, professor_id)
VALUES (?, ?, ?, ?, ?)
''', courses)

# Insert sample data into Students
students = [
    ('Emily Davis', 'emily.davis@student.edu', '555-8765', '2001-05-12'),
    ('Michael Brown', 'michael.brown@student.edu', '555-4321', '2000-11-30'),
    ('Sarah Johnson', 'sarah.johnson@student.edu', '555-1357', '2002-08-22'),
    ('David Smith', 'david.smith@student.edu', '555-2468', '2001-12-11'),
    ('Laura Wilson', 'laura.wilson@student.edu', '555-3579', '2000-03-29'),
    ('James Lee', 'james.lee@student.edu', '555-4680', '2002-07-15'),
    ('Linda White', 'linda.white@student.edu', '555-5791', '2001-10-04'),
    ('Robert Green', 'robert.green@student.edu', '555-6802', '2002-06-23'),
    ('Jessica Brown', 'jessica.brown@student.edu', '555-7913', '2000-09-12'),
    ('William Harris', 'william.harris@student.edu', '555-8024', '2001-04-19'),
    ('Emma Clark', 'emma.clark@student.edu', '555-9135', '2002-11-02'),
    ('Olivia Lewis', 'olivia.lewis@student.edu', '555-0246', '2000-12-31'),
    ('Daniel Martin', 'daniel.martin@student.edu', '555-1358', '2001-06-14'),
    ('Sophia Walker', 'sophia.walker@student.edu', '555-2469', '2002-03-05'),
    ('Matthew Young', 'matthew.young@student.edu', '555-3570', '2001-08-20')
]
cursor.executemany('''
INSERT OR IGNORE INTO Students (name, email, phone, date_of_birth)
VALUES (?, ?, ?, ?)
''', students)


# Commit and close the connection
conn.commit()
conn.close()

print("Database schema with Grades and Course Requests created and sample data inserted successfully.")

# Function to get a connection to the SQLite database
def get_connection():
    return sqlite3.connect('university_results1.db')

# Functions for Managing Students
def add_student(name, email, phone, date_of_birth):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Students (name, email, phone, date_of_birth)
    VALUES (?, ?, ?, ?)
    ''', (name, email, phone, date_of_birth))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM Students
    WHERE student_id = ?
    ''', (student_id,))
    conn.commit()
    conn.close()

def update_student(student_id, name=None, email=None, phone=None, date_of_birth=None):
    conn = get_connection()
    cursor = conn.cursor()
    if name:
        cursor.execute('''
        UPDATE Students
        SET name = ?
        WHERE student_id = ?
        ''', (name, student_id))
    if email:
        cursor.execute('''
        UPDATE Students
        SET email = ?
        WHERE student_id = ?
        ''', (email, student_id))
    if phone:
        cursor.execute('''
        UPDATE Students
        SET phone = ?
        WHERE student_id = ?
        ''', (phone, student_id))
    if date_of_birth:
        cursor.execute('''
        UPDATE Students
        SET date_of_birth = ?
        WHERE student_id = ?
        ''', (date_of_birth, student_id))
    conn.commit()
    conn.close()

# Functions for Managing Courses
def add_course(course_name, course_code, credits, department, professor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Courses (course_name, course_code, credits, department, professor_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (course_name, course_code, credits, department, professor_id))
    conn.commit()
    conn.close()

def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM Courses
    WHERE course_id = ?
    ''', (course_id,))
    conn.commit()
    conn.close()

def update_course(course_id, course_name=None, course_code=None, credits=None, department=None, professor_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if course_name:
        cursor.execute('''
        UPDATE Courses
        SET course_name = ?
        WHERE course_id = ?
        ''', (course_name, course_id))
    if course_code:
        cursor.execute('''
        UPDATE Courses
        SET course_code = ?
        WHERE course_id = ?
        ''', (course_code, course_id))
    if credits:
        cursor.execute('''
        UPDATE Courses
        SET credits = ?
        WHERE course_id = ?
        ''', (credits, course_id))
    if department:
        cursor.execute('''
        UPDATE Courses
        SET department = ?
        WHERE course_id = ?
        ''', (department, course_id))
    if professor_id is not None:
        cursor.execute('''
        UPDATE Courses
        SET professor_id = ?
        WHERE course_id = ?
        ''', (professor_id, course_id))
    conn.commit()
    conn.close()

# Functions for Managing Professors
def add_professor(name, email, department, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Professors (name, email, department, phone)
    VALUES (?, ?, ?, ?)
    ''', (name, email, department, phone))
    conn.commit()
    conn.close()

def delete_professor(professor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM Professors
    WHERE professor_id = ?
    ''', (professor_id,))
    conn.commit()
    conn.close()

def update_professor(professor_id, name=None, email=None, department=None, phone=None):
    conn = get_connection()
    cursor = conn.cursor()
    if name:
        cursor.execute('''
        UPDATE Professors
        SET name = ?
        WHERE professor_id = ?
        ''', (name, professor_id))
    if email:
        cursor.execute('''
        UPDATE Professors
        SET email = ?
        WHERE professor_id = ?
        ''', (email, professor_id))
    if department:
        cursor.execute('''
        UPDATE Professors
        SET department = ?
        WHERE professor_id = ?
        ''', (department, professor_id))
    if phone:
        cursor.execute('''
        UPDATE Professors
        SET phone = ?
        WHERE professor_id = ?
        ''', (phone, professor_id))
    conn.commit()
    conn.close()
    
 
def display_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Students
    ''')
    
    # Fetch all the rows
    students = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in students:
        print(i)
        
    conn.close()
    
def display_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Courses
    ''')
    
    # Fetch all the rows
    courses = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in courses:
        print(i)
        
    conn.close()
    
def display_all_professors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Professors
    ''')
    
    # Fetch all the rows
    professors = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in professors:
        print(i)
        
    conn.close()
    
def display_all_requests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Course_Requests
    ''')
    
    # Fetch all the rows
    requests = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in requests:
        print(i)
        
    conn.close() 
    
def display_all_grades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Grades
    ''')
    
    # Fetch all the rows
    grades = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in grades:
        print(i)
        
    conn.close() 
    
def display_all_enrollments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM Enrollments
    ''')
    
    # Fetch all the rows
    enrollments = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in enrollments:
        print(i)
        
    conn.close()                 
    
# def request_course(student_id, course_id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Check if the course exists
#     cursor.execute('''
#     SELECT credits FROM Courses
#     WHERE course_id = ?
#     ''', (course_id,))
#     course = cursor.fetchone()
#     if not course:
#         print("Course does not exist.")
#         conn.close()
#         return

#     course_credits = course[0]

#     # Check if the student has already requested this course
#     cursor.execute('''
#     SELECT request_id FROM Course_Requests
#     WHERE student_id = ? AND course_id = ? AND status IS NULL
#     ''', (student_id, course_id))
#     existing_request = cursor.fetchone()
#     if existing_request:
#         print("Course request already exists and is pending.")
#         conn.close()
#         return

#     # Calculate total credits of all current requests for this student
#     cursor.execute('''
#     SELECT SUM(Courses.credits) 
#     FROM Course_Requests 
#     JOIN Courses ON Course_Requests.course_id = Courses.course_id
#     WHERE Course_Requests.student_id = ? AND Course_Requests.status IS NULL
#     ''', (student_id,))
#     total_credits = cursor.fetchone()[0] or 0

#     # Check if adding this course would exceed the 20 credits limit
#     if total_credits + course_credits > 20:
#         print("Adding this course would exceed the 20-credit limit.")
#         conn.close()
#         return

#     # Request the course
#     cursor.execute('''
#     INSERT INTO Course_Requests (student_id, course_id, request_date, status)
#     VALUES (?, ?, DATE('now'), NULL)
#     ''', (student_id, course_id))
#     conn.commit()
#     conn.close()

#     print("Course request submitted successfully.")


# def manage_course_request(request_id, professor_id, action):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Check if the request exists and get the details
#     cursor.execute('''
#     SELECT student_id, course_id FROM Course_Requests
#     WHERE request_id = ?
#     ''', (request_id,))
#     request = cursor.fetchone()

#     if not request:
#         print("Request does not exist.")
#         conn.close()
#         return

#     student_id, course_id = request

#     # Check if the professor is assigned to the course
#     cursor.execute('''
#     SELECT professor_id FROM Courses
#     WHERE course_id = ?
#     ''', (course_id,))
#     course = cursor.fetchone()

#     if not course:
#         print("Course does not exist.")
#         conn.close()
#         return

#     assigned_professor_id = course[0]

#     if assigned_professor_id != professor_id:
#         print("You are not authorized to manage this course request.")
#         conn.close()
#         return

#     if action == 'accept':
#         # Move the request to the Enrollments table
#         cursor.execute('''
#         INSERT INTO Enrollments (student_id, course_id)
#         VALUES (?, ?)
#         ''', (student_id, course_id))

#         # Delete the request from Course_Requests
#         cursor.execute('''
#         DELETE FROM Course_Requests
#         WHERE request_id = ?
#         ''', (request_id,))

#         conn.commit()
#         print("Course request accepted and enrollment completed.")
#     elif action == 'reject':
#         # Delete the request from Course_Requests
#         cursor.execute('''
#         DELETE FROM Course_Requests
#         WHERE request_id = ?
#         ''', (request_id,))

#         conn.commit()
#         print("Course request rejected.")
#     else:
#         print("Invalid action. Please use 'accept' or 'reject'.")

#     conn.close()


def request_course(student_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the course exists
    cursor.execute('''
    SELECT credits FROM Courses
    WHERE course_id = ?
    ''', (course_id,))
    course = cursor.fetchone()
    if not course:
        print("Course does not exist.")
        conn.close()
        return

    course_credits = course[0]

    # Check if the student is already enrolled in this course
    cursor.execute('''
    SELECT * FROM Enrollments
    WHERE student_id = ? AND course_id = ?
    ''', (student_id, course_id))
    enrollment = cursor.fetchone()
    if enrollment:
        print("Student is already enrolled in this course.")
        conn.close()
        return

    # Check if the student has a rejected request for this course
    cursor.execute('''
    SELECT status FROM Course_Requests
    WHERE student_id = ? AND course_id = ?
    ''', (student_id, course_id))
    existing_request = cursor.fetchone()
    if existing_request:
        status = existing_request[0]
        if status == 'rejected':
            print("Previous request for this course was rejected. Cannot request again.")
            conn.close()
            return

    # Check if the student has already requested this course and it's pending
    cursor.execute('''
    SELECT request_id FROM Course_Requests
    WHERE student_id = ? AND course_id = ? AND status = 'pending'
    ''', (student_id, course_id))
    existing_request = cursor.fetchone()
    if existing_request:
        print("Course request already exists and is pending.")
        conn.close()
        return

    # Calculate total credits of all current requests for this student
    cursor.execute('''
    SELECT SUM(Courses.credits) 
    FROM Course_Requests 
    JOIN Courses ON Course_Requests.course_id = Courses.course_id
    WHERE Course_Requests.student_id = ? AND Course_Requests.status IS NULL
    ''', (student_id,))
    total_credits = cursor.fetchone()[0] or 0

    # Check if adding this course would exceed the 20 credits limit
    if total_credits + course_credits > 20:
        print("Adding this course would exceed the 20-credit limit.")
        conn.close()
        return

    # Request the course
    cursor.execute('''
    INSERT INTO Course_Requests (student_id, course_id, request_date, status)
    VALUES (?, ?, DATE('now'), 'pending')
    ''', (student_id, course_id))
    
    conn.commit()
    conn.close()

    print("Course request submitted successfully.")


def manage_course_request(request_id, professor_id, action):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the request exists and get the details
    cursor.execute('''
    SELECT student_id, course_id, status FROM Course_Requests
    WHERE request_id = ?
    ''', (request_id,))
    request = cursor.fetchone()

    if not request:
        print("Request does not exist.")
        conn.close()
        return

    student_id, course_id, current_status = request

    # Check if the professor is assigned to the course
    cursor.execute('''
    SELECT professor_id FROM Courses
    WHERE course_id = ?
    ''', (course_id,))
    course = cursor.fetchone()

    if not course:
        print("Course does not exist.")
        conn.close()
        return

    assigned_professor_id = course[0]

    if assigned_professor_id != professor_id:
        print("You are not authorized to manage this course request.")
        conn.close()
        return

    # if current_status:
    #     print(f"Request already has status '{current_status}'. Cannot change.")
    #     conn.close()
    #     return

    if action == 'accept':
        # Check if the request has already been accepted or rejected
        if current_status == 'accepted':
            print("Course request has already been accepted.")
        else:
            # Add the request to the Enrollments table
            cursor.execute('''
            INSERT INTO Enrollments (student_id, course_id)
            VALUES (?, ?)
            ''', (student_id, course_id))

            # Update the status of the request in Course_Requests
            cursor.execute('''
            UPDATE Course_Requests
            SET status = 'accepted'
            WHERE request_id = ?
            ''', (request_id,))

            conn.commit()
            print("Course request accepted and enrollment completed.")

    elif action == 'reject':
        # Check if the request has already been accepted or rejected
        if current_status == 'rejected':
            print("Course request has already been rejected.")
        else:
            # Update the status of the request in Course_Requests
            cursor.execute('''
            UPDATE Course_Requests
            SET status = 'rejected'
            WHERE request_id = ?
            ''', (request_id,))

            conn.commit()
            print("Course request rejected.")

    else:
        print("Invalid action. Please use 'accept' or 'reject'.")

    conn.close()


def show_all_requests_for_professor(professor_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve all course IDs managed by the professor
    cursor.execute('''
    SELECT course_id FROM Courses
    WHERE professor_id = ?
    ''', (professor_id,))
    courses = cursor.fetchall()

    if not courses:
        print("No courses found for this professor.")
        conn.close()
        return

    course_ids = [course[0] for course in courses]

    # Retrieve all requests for these courses
    cursor.execute('''
    SELECT Course_Requests.request_id, Course_Requests.student_id, Course_Requests.course_id, Students.name AS student_name, Courses.course_name
    FROM Course_Requests
    JOIN Courses ON Course_Requests.course_id = Courses.course_id
    JOIN Students ON Course_Requests.student_id = Students.student_id
    WHERE Course_Requests.course_id IN ({})
    '''.format(','.join('?' * len(course_ids))), course_ids)

    requests = cursor.fetchall()
    conn.close()

    if not requests:
        print("No course requests found for the professor's courses.")
        return

    print("Course Requests for Courses Managed by Professor ID", professor_id)
    print("Request ID | Student ID | Student Name | Course ID | Course Name")
    for request in requests:
        print(f"{request[0]} | {request[1]} | {request[3]} | {request[2]} | {request[4]}")


def student_dashboard(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the student's course requests with course details and professor names
    cursor.execute('''
    SELECT Course_Requests.request_id, Courses.course_id, Courses.course_name, Professors.name AS professor_name, Course_Requests.status
    FROM Course_Requests
    JOIN Courses ON Course_Requests.course_id = Courses.course_id
    JOIN Professors ON Courses.professor_id = Professors.professor_id
    WHERE Course_Requests.student_id = ?
    ''', (student_id,))

    requests = cursor.fetchall()
    conn.close()

    if not requests:
        print("No pending course requests found.")
        return


    
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in requests:
        print(i)

def students_in_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the students enrolled in the specified course
    cursor.execute('''
    SELECT Enrollments.student_id, Students.name
    FROM Enrollments
    JOIN Students ON Enrollments.student_id = Students.student_id
    WHERE Enrollments.course_id = ?
    ''', (course_id,))

    enrollments = cursor.fetchall()
    conn.close()

    if not enrollments:
        print(f"No students enrolled in course with ID {course_id}.")
        return

    column_names = [description[0] for description in cursor.description]
    
    # Print the column names
    print(column_names)
  
    for i in enrollments:
        print(i)


def export_students_in_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the students enrolled in the specified course
    cursor.execute('''
    SELECT Enrollments.student_id, Students.name
    FROM Enrollments
    JOIN Students ON Enrollments.student_id = Students.student_id
    WHERE Enrollments.course_id = ?
    ''', (course_id,))

    enrollments = cursor.fetchall()
    conn.close()

    if not enrollments:
        print(f"No students enrolled in course with ID {course_id}.")
        return

    # Convert data to a DataFrame
    df = pd.DataFrame(enrollments, columns=['Student ID', 'Student Name'])

    # Save DataFrame to Excel file
    file_name = f"{course_id}.xlsx"
    df.to_excel(file_name, index=False, engine='openpyxl')

    print(f"Students enrolled in Course ID {course_id} have been exported to '{file_name}'.")


def add_grade(professor_id, course_id, student_id, grade):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the professor is assigned to the course
    cursor.execute('''
    SELECT professor_id FROM Courses
    WHERE course_id = ?
    ''', (course_id,))
    course = cursor.fetchone()

    if not course:
        print("Course does not exist.")
        conn.close()
        return

    assigned_professor_id = course[0]

    if assigned_professor_id != professor_id:
        print("You are not authorized to add grades for this course.")
        conn.close()
        return

    # Check if the student is enrolled in the course
    cursor.execute('''
    SELECT enrollment_id FROM Enrollments
    WHERE course_id = ? AND student_id = ?
    ''', (course_id, student_id))
    enrollment = cursor.fetchone()

    if not enrollment:
        print("Student is not enrolled in this course.")
        conn.close()
        return

    enrollment_id = enrollment[0]

    # Add or update the grade
    cursor.execute('''
    INSERT INTO Grades (course_id, student_id, grade, grade_date)
    VALUES (?, ?, ?, DATE('now'))
    ON CONFLICT(course_id, student_id)
    DO UPDATE SET grade = excluded.grade, grade_date = excluded.grade_date
    ''', (course_id, student_id, grade))

    conn.commit()
    conn.close()

    print(f"Grade for student ID {student_id} in course ID {course_id} has been added/updated.")
    
    
def student_results(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve courses and grades for the student
    cursor.execute('''
    SELECT Courses.course_id, Courses.course_code, Courses.course_name, Courses.credits, Grades.grade
    FROM Enrollments
    JOIN Courses ON Enrollments.course_id = Courses.course_id
    LEFT JOIN Grades ON Courses.course_id = Grades.course_id AND Enrollments.student_id = Grades.student_id
    WHERE Enrollments.student_id = ?
    ''', (student_id,))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No results found for student ID {student_id}.")
        return

    print(f"Results for Student ID {student_id}:")
    print("Course ID | Course Code | Course Name | Credits | Grade")
    for result in results:
        print(f"{result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4] if result[4] else 'Not Graded'}")
    



def generate_report_card(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve student personal information
    cursor.execute('''
    SELECT student_id, name, email, phone FROM Students
    WHERE student_id = ?
    ''', (student_id,))
    student_info = cursor.fetchone()

    if not student_info:
        print(f"No personal information found for student ID {student_id}.")
        conn.close()
        return

    student_id, name, email, phone = student_info

    # Retrieve courses and grades for the student
    cursor.execute('''
    SELECT Courses.course_id, Courses.course_code, Courses.course_name, Courses.credits, Grades.grade
    FROM Enrollments
    JOIN Courses ON Enrollments.course_id = Courses.course_id
    LEFT JOIN Grades ON Courses.course_id = Grades.course_id AND Enrollments.student_id = Grades.student_id
    WHERE Enrollments.student_id = ?
    ''', (student_id,))

    results = cursor.fetchall()
    conn.close()

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add Student Personal Information
    pdf.cell(0, 10, f"Student Report Card - ID: {student_id}", ln=True, align="C")
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Phone: {phone}", ln=True)
    pdf.ln(10)

    # Add Course Grades Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Course ID", 1)
    pdf.cell(40, 10, "Course Code", 1)
    pdf.cell(60, 10, "Course Name", 1)
    pdf.cell(20, 10, "Credits", 1)
    pdf.cell(30, 10, "Grade", 1)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for result in results:
        pdf.cell(40, 10, str(result[0]), 1)
        pdf.cell(40, 10, result[1], 1)
        pdf.cell(60, 10, result[2], 1)
        pdf.cell(20, 10, str(result[3]), 1)
        pdf.cell(30, 10, result[4] if result[4] else 'Not Graded', 1)
        pdf.ln()

    # Save the PDF
    file_name = f"Student_{student_id}_Report_Card.pdf"
    pdf.output(file_name)

    print(f"Report card for student ID {student_id} has been generated and saved as '{file_name}'.")



# request_course(1,1)
# request_course(1,2)
# request_course(1,3)
# request_course(1,4)
# request_course(2,1)
# request_course(3,1)

# manage_course_request(5,1,'accept')
# manage_course_request(6,1,'accept')

# student_dashboard(1)

# students_in_course(1)

# export_students_in_course(1)

# add_grade(1,1,1,'A')
# add_grade(1,1,2,'C')
# add_grade(1,1,3,'B')

# student_results(1)

generate_report_card(1)
