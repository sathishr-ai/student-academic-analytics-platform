import sqlite3
import pandas as pd
import numpy as np
import os

def generate_sample_dataset(num_students=1500):
    """Generate sample dataset using the original logic."""
    np.random.seed(42)

    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
                  'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
                  'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
                  'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
                  'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']

    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
                 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
                 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores']

    majors = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Chemistry',
             'Engineering', 'Business', 'Economics', 'Psychology', 'History',
             'English', 'Political Science', 'Sociology', 'Art', 'Music']

    courses = {
        'Computer Science': ['CS101', 'CS102', 'CS201', 'CS202', 'CS301', 'CS302', 'CS401', 'CS402'],
        'Mathematics': ['MATH101', 'MATH102', 'MATH201', 'MATH202', 'MATH301', 'MATH302', 'MATH401', 'MATH402'],
        'Physics': ['PHYS101', 'PHYS102', 'PHYS201', 'PHYS202', 'PHYS301', 'PHYS302', 'PHYS401', 'PHYS402'],
        'Biology': ['BIO101', 'BIO102', 'BIO201', 'BIO202', 'BIO301', 'BIO302', 'BIO401', 'BIO402'],
        'Chemistry': ['CHEM101', 'CHEM102', 'CHEM201', 'CHEM202', 'CHEM301', 'CHEM302', 'CHEM401', 'CHEM402'],
        'Engineering': ['ENG101', 'ENG102', 'ENG201', 'ENG202', 'ENG301', 'ENG302', 'ENG401', 'ENG402'],
        'Business': ['BUS101', 'BUS102', 'BUS201', 'BUS202', 'BUS301', 'BUS302', 'BUS401', 'BUS402'],
        'Economics': ['ECON101', 'ECON102', 'ECON201', 'ECON202', 'ECON301', 'ECON302', 'ECON401', 'ECON402'],
        'Psychology': ['PSY101', 'PSY102', 'PSY201', 'PSY202', 'PSY301', 'PSY302', 'PSY401', 'PSY402'],
        'History': ['HIST101', 'HIST102', 'HIST201', 'HIST202', 'HIST301', 'HIST302', 'HIST401', 'HIST402'],
        'English': ['ENG101', 'ENG102', 'ENG201', 'ENG202', 'ENG301', 'ENG302', 'ENG401', 'ENG402'],
        'Political Science': ['POL101', 'POL102', 'POL201', 'POL202', 'POL301', 'POL302', 'POL401', 'POL402'],
        'Sociology': ['SOC101', 'SOC102', 'SOC201', 'SOC202', 'SOC301', 'SOC302', 'SOC401', 'SOC402'],
        'Art': ['ART101', 'ART102', 'ART201', 'ART202', 'ART301', 'ART302', 'ART401', 'ART402'],
        'Music': ['MUS101', 'MUS102', 'MUS201', 'MUS202', 'MUS301', 'MUS302', 'MUS401', 'MUS402']
    }

    course_credits = {'101': 3, '102': 3, '201': 4, '202': 4, '301': 3, '302': 3, '401': 4, '402': 4}

    data = []
    student_id = 1000

    for _ in range(num_students):
        student_id += 1
        first_name = np.random.choice(first_names)
        last_name = np.random.choice(last_names)
        major = np.random.choice(majors)
        department = major

        birth_year = np.random.randint(1998, 2003)
        birth_month = np.random.randint(1, 12)
        birth_day = np.random.randint(1, 28)
        enroll_year = birth_year + 18
        enroll_month = np.random.choice([1, 9])
        enroll_day = np.random.randint(1, 28)

        date_of_birth = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        enrollment_date = f"{enroll_year}-{enroll_month:02d}-{enroll_day:02d}"
        email = f"{first_name.lower()}.{last_name.lower()}{student_id}@university.edu"
        phone = f"555-{np.random.randint(1000, 9999)}"

        num_courses = np.random.randint(4, 8)
        student_courses = np.random.choice(courses[major], min(num_courses, len(courses[major])), replace=False)

        for course_code in student_courses:
            course_level = int(course_code[-3:-1])
            if course_level <= 102:
                year = enroll_year
                semester = 'Fall' if enroll_month == 9 else 'Spring'
            elif course_level <= 202:
                year = enroll_year + 1
                semester = np.random.choice(['Fall', 'Spring'])
            elif course_level <= 302:
                year = enroll_year + 2
                semester = np.random.choice(['Fall', 'Spring'])
            else:
                year = enroll_year + 3
                semester = np.random.choice(['Fall', 'Spring'])

            base_grade = np.random.normal(3.0, 0.8)
            grade = max(0, min(4.0, base_grade))
            base_attendance = np.random.normal(0.85, 0.1)
            attendance = max(0.5, min(1.0, base_attendance))

            if attendance > 0.9: grade = min(4.0, grade + 0.3)
            elif attendance < 0.7: grade = max(0, grade - 0.3)

            credits = course_credits[course_code[-3:]]
            course_name = f"{course_code} Course"

            data.append({
                'student_id': student_id,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth,
                'enrollment_date': enrollment_date,
                'major': major,
                'email': email,
                'phone': phone,
                'course_code': course_code,
                'course_name': course_name,
                'credits': credits,
                'department': department,
                'semester': semester,
                'year': year,
                'grade': round(grade, 2),
                'attendance': round(attendance, 2)
            })

    return pd.DataFrame(data)

def seed_database():
    print("Generating 1,500 sample student records...")
    df = generate_sample_dataset()
    
    # Normalize Data into 3 Tables
    print("Normalizing data into Students, Courses, and Enrollments...")
    
    # 1. Students Table
    students_df = df[['student_id', 'first_name', 'last_name', 'date_of_birth', 'enrollment_date', 'major', 'email', 'phone']].drop_duplicates(subset=['student_id'])
    
    # 2. Courses Table
    courses_df = df[['course_code', 'course_name', 'credits', 'department']].drop_duplicates(subset=['course_code'])
    
    # 3. Enrollments Table
    enrollments_df = df[['student_id', 'course_code', 'semester', 'year', 'grade', 'attendance']]
    
    # Connect and insert to SQLite
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'student_data.db')
    print(f"Connecting to SQLite database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Write tables (replace if exists to allow easy re-seeding)
        students_df.to_sql('Students', conn, if_exists='replace', index=False)
        courses_df.to_sql('Courses', conn, if_exists='replace', index=False)
        enrollments_df.to_sql('Enrollments', conn, if_exists='replace', index=False)
        print("✅ Successfully seeded SQLite Database with 3 normalized tables.")
        
        # Verify
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students")
        print(f"Students Total: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM Enrollments")
        print(f"Enrollments Total: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()
