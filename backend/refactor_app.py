import sys

filepath = r'c:\Users\SATHISH\Downloads\Student academic analytics platform\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '# Core Student Records System Class (adapted for web)'
end_marker = '# Plotting functions'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_class = '''# Core Student Records System Class (SQL wrapper)
# ------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.database import DatabaseManager
import pandas as pd
import numpy as np

class StudentRecordsSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.data = pd.DataFrame()
        self.student_details_cache = {}

    def load_data(self, file=None):
        """Load data from SQLite or CSV fallback"""
        if file is not None:
            try:
                self.data = pd.read_csv(file)
                self.clean_data()
            except Exception as e:
                import streamlit as st
                st.error(f"Error loading CSV: {e}")
                return False
        else:
            self.data = self.db.get_all_student_data()
        
        return True

    def clean_data(self):
        """Clean data only if loaded from external CSV (SQLite data is already clean)"""
        if self.data is None or self.data.empty:
            return

        self.data.fillna({
            'major': 'Undeclared',
            'attendance': self.data['attendance'].mean(),
            'grade': self.data['grade'].mean()
        }, inplace=True)

        date_columns = ['date_of_birth', 'enrollment_date']
        for col in date_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_datetime(self.data[col], errors='coerce')

        Q1 = self.data['grade'].quantile(0.25)
        Q3 = self.data['grade'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        self.data['grade'] = np.where(self.data['grade'] < lower_bound, lower_bound, self.data['grade'])
        self.data['grade'] = np.where(self.data['grade'] > upper_bound, upper_bound, self.data['grade'])

    def get_student_details(self, identifier):
        """Return student details and course history via DB"""
        return self.db.get_student_details(identifier)

    def dataset_statistics(self):
        """Return overall dataset stats from in-memory dataframe"""
        if self.data is None or self.data.empty:
            return {}
        stats = {
            'total_records': len(self.data),
            'unique_students': self.data['student_id'].nunique(),
            'unique_courses': self.data['course_code'].nunique(),
            'min_year': int(self.data['year'].min()),
            'max_year': int(self.data['year'].max()),
            'avg_gpa': float(self.data['grade'].mean()),
            'avg_attendance': float(self.data['attendance'].mean()),
            'top_majors': self.data[['student_id', 'major']].drop_duplicates()['major'].value_counts().head(5).to_dict()
        }
        return stats

# ------------------------------
'''
    new_text = text[:start_idx] + new_class + text[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully replaced StudentRecordsSystem with SQLite wrapper in app.py")
else:
    print(f"Error: Could not find markers. start_idx: {start_idx}, end_idx: {end_idx}")
