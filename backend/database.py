import sqlite3
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, db_path='student_data.db'):
        # Get the absolute path to the db file relative to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_path)
        
        # Auto-seed the database if it doesn't exist (e.g. on Streamlit Cloud)
        if not os.path.exists(self.db_path):
            print(f"Database {self.db_path} missing. Running auto-seeder...")
            from backend.seed_data import seed_database
            seed_database()
    
    def get_connection(self):
        """Create and return a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            # Enable returning rows as dictionaries
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def get_all_student_data(self):
        """
        Fetch all unified student and course data into a Pandas DataFrame.
        This mimics the structure of the original in-memory dataset for seamless integration.
        """
        query = """
        SELECT 
            s.student_id, s.first_name, s.last_name, s.date_of_birth, s.enrollment_date, 
            s.major, s.email, s.phone,
            c.course_code, c.course_name, c.credits, c.department,
            e.semester, e.year, e.grade, e.attendance
        FROM 
            Students s
        JOIN 
            Enrollments e ON s.student_id = e.student_id
        JOIN 
            Courses c ON e.course_code = c.course_code
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame() # Return empty DF on failure

    def get_student_details(self, identifier):
        """
        Fetch details for a specific student given an ID or Name.
        Returns a tuple of (student_summary_df, detailed_course_history_df)
        """
        df = self.get_all_student_data()
        if df.empty:
            return None, None

        # Try searching by ID
        try:
            student_id = int(identifier)
            student_data = df[df['student_id'] == student_id]
        except ValueError:
            # Search by name
            student_data = df[
                (df['first_name'].str.contains(identifier, case=False, na=False)) |
                (df['last_name'].str.contains(identifier, case=False, na=False))
            ]

        if student_data.empty:
            return None, None

        unique_students = student_data[['student_id', 'first_name', 'last_name', 'date_of_birth',
                                      'enrollment_date', 'major', 'email', 'phone']].drop_duplicates()

        student_stats = student_data.groupby('student_id').agg({
            'grade': 'mean',
            'attendance': 'mean',
            'credits': 'sum'
        }).reset_index()
        student_stats.rename(columns={'grade': 'cgpa', 'attendance': 'overall_attendance'}, inplace=True)

        student_details = unique_students.merge(student_stats, on='student_id')
        return student_details, student_data
