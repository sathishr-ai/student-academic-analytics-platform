# app.py - Student Academic Analytics Platform (Streamlit Web App)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import os
import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Student Analytics Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Hero Header ─────────────────────────── */
.hero-title {
    font-size: 3rem; font-weight: 800; letter-spacing: -1.5px;
    background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 50%, #34D399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 0.2rem;
}
.hero-sub {
    font-size: 1.05rem; color: #94A3B8; text-align: center;
    margin-bottom: 2.5rem; font-weight: 400;
}


/* ── Metric / Info Cards ──────────────────── */
.metric-card {
    background: rgba(15,23,42,0.65); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 18px;
    padding: 1.5rem 1.4rem; text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,.04);
    transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s ease, border-color .3s ease;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content:''; position:absolute; top:0; left:-100%; width:100%; height:100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.03), transparent);
    transition: left .6s ease;
}
.metric-card:hover::before { left: 100%; }
.metric-card:hover { transform: translateY(-6px); box-shadow: 0 12px 36px rgba(96,165,250,0.2), inset 0 1px 0 rgba(255,255,255,.06); border-color: rgba(96,165,250,.2); }
.metric-card h3 { margin:0; font-size:.78rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:1.2px; }
.metric-card p  { margin:.5rem 0 0; font-size:2.4rem; font-weight:800; color:#F1F5F9; letter-spacing:-0.5px; }
.metric-card .sub { font-size:.78rem; color:#64748B; margin-top:.3rem; }

.danger-card  { border-left: 4px solid #EF4444 !important; }
.warning-card { border-left: 4px solid #F59E0B !important; }
.success-card { border-left: 4px solid #10B981 !important; }
.info-card    { border-left: 4px solid #3B82F6 !important; }

/* ── Status Pills ─────────────────────────── */
.pill { display:inline-block; padding:2px 10px; border-radius:999px; font-size:.75rem; font-weight:600; }
.pill-red    { background:rgba(239,68,68,.15);  color:#FCA5A5; border:1px solid rgba(239,68,68,.3); }
.pill-yellow { background:rgba(245,158,11,.15); color:#FCD34D; border:1px solid rgba(245,158,11,.3); }
.pill-green  { background:rgba(16,185,129,.15); color:#6EE7B7; border:1px solid rgba(16,185,129,.3); }
.pill-blue   { background:rgba(59,130,246,.15); color:#93C5FD; border:1px solid rgba(59,130,246,.3); }

/* ── Student Info Box ─────────────────────── */
.student-info {
    background:rgba(30,41,59,0.6); border:1px solid rgba(255,255,255,0.05);
    color:#F3F4F6; padding:1.6rem; border-radius:12px;
    border-left:5px solid #3B82F6; margin-bottom:1.5rem;
}
.student-info h3 { margin-top:0; color:#60A5FA; font-weight:700; }
.student-info strong { color:#94A3B8; font-weight:500; }

/* ── Landing page cards ───────────────────── */
.feature-card {
    background:rgba(30,41,59,0.5); border:1px solid rgba(255,255,255,0.06);
    border-radius:14px; padding:1.4rem 1.2rem; text-align:center;
    transition: transform .2s, box-shadow .2s;
}
.feature-card:hover { transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,0.3); }
.feature-icon { font-size:2rem; margin-bottom:.5rem; }
.feature-title { font-weight:700; color:#E2E8F0; font-size:1rem; }
.feature-desc  { font-size:.83rem; color:#64748B; margin-top:.3rem; }

/* ── Buttons ──────────────────────────────── */
div.stButton > button:first-child {
    background:linear-gradient(135deg,#3B82F6,#2563EB); color:white;
    border:none; border-radius:8px; padding:.55rem 2rem;
    font-weight:600; box-shadow:0 4px 12px rgba(37,99,235,.35);
    transition:all .25s ease;
}
div.stButton > button:first-child:hover {
    background:linear-gradient(135deg,#60A5FA,#3B82F6);
    box-shadow:0 6px 18px rgba(37,99,235,.5); transform:translateY(-2px);
}

/* ── Tabs ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { gap:6px; }
.stTabs [data-baseweb="tab"] { border-radius:6px 6px 0 0; padding:10px 18px 14px; font-weight:600; background:transparent; }
.stTabs [aria-selected="true"] { color:#60A5FA !important; border-bottom-color:#3B82F6 !important; }

/* ── Inputs ───────────────────────────────── */
.stTextInput input, .stSelectbox > div > div {
    background:rgba(30,41,59,.55) !important; border:1px solid rgba(255,255,255,.1) !important;
    color:white !important; border-radius:8px !important;
}
.stTextInput input:focus { border-color:#3B82F6 !important; box-shadow:0 0 0 1px #3B82F6 !important; }

/* ── Streamlit Core UI Hidden (Clean App Feel) ───────────────── */
/* We hide the header background and decorative elements, but KEEP the sidebar toggle */
[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}

/* Hide Deploy, Menu, and Status Widget but NOT the sidebar buttons */
.stDeployButton, #MainMenu, [data-testid="stStatusWidget"], footer {
    visibility: hidden !important;
    display: none !important;
    height: 0 !important;
    width: 0 !important;
}

/* Ensure Sidebar toggle buttons are EXTREMELY visible (Floating Action Button style) */
/* Targeted selectors for both states (Expanded & Collapsed) */
div[data-testid="stSidebarCollapsedControl"] button, 
div[data-testid="stSidebarCollapseButton"] button,
button[aria-label="Expand sidebar"],
button[aria-label="Collapse sidebar"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    background: #2563EB !important; /* Bright solid blue */
    color: white !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    padding: 0px !important;
    margin: 10px !important;
    border: 2px solid rgba(255,255,255,0.4) !important;
    box-shadow: 0 4px 20px rgba(37,99,235,0.8) !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    z-index: 99999999 !important;
    justify-content: center !important;
    align-items: center !important;
    cursor: pointer !important;
}

/* Force the icon inside to be white and bold */
div[data-testid="stSidebarCollapsedControl"] button svg, 
div[data-testid="stSidebarCollapseButton"] button svg,
button[aria-label="Expand sidebar"] svg,
button[aria-label="Collapse sidebar"] svg {
    fill: white !important;
    color: white !important;
    width: 30px !important;
    height: 30px !important;
    stroke: white !important;
    stroke-width: 3px !important;
}

div[data-testid="stSidebarCollapsedControl"] button:hover, 
div[data-testid="stSidebarCollapseButton"] button:hover {
    background: #1D4ED8 !important;
    transform: scale(1.2) rotate(15deg) !important;
    box-shadow: 0 8px 35px rgba(37,99,235,0.9) !important;
}

/* Fix Sidebar visibility and container z-index */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0F1E 0%, #0D1427 60%, #0A1128 100%) !important;
    border-right: 1px solid rgba(96,165,250,0.12) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
    visibility: visible !important;
    z-index: 99999998 !important;
}
[data-testid="stSidebar"][aria-expanded="true"] {
    width: 280px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0rem 0.6rem 1rem !important;
}

/* Hide all radio button circles */
.stRadio > div > div > label > div:first-child { display: none !important; }

/* ── Nav Item Base Style ───────────────────── */
.stRadio > div > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1rem !important;
    border-radius: 12px !important;
    margin-bottom: 4px !important;
    cursor: pointer !important;
    border: 1px solid transparent !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    color: #94A3B8 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    line-height: 1.4 !important;
    background: transparent !important;
    position: relative !important;
    overflow: hidden !important;
}

/* ── Sidebar Radio Navigation (Custom "One Point" Style) ── */
section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { 
    gap: 0 !important; 
}

/* 1. Base label styling for all sidebar radio items */
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 0.45rem 0.6rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin: 1px 0 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
}

/* 2. COMPLETELY HIDE ALL default radio icons and their containers in the sidebar */
section[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stRadioButton"],
section[data-testid="stSidebar"] [data-testid="stRadio"] div[class*="StyledRadioButton"],
section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* 3. Base Dot Style (The "One Point") - Hidden by default, enabled per item index below */
section[data-testid="stSidebar"] [data-testid="stRadio"] label::before {
    content: '';
    display: none !important;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: transparent;
    border: 1.5px solid #475569;
    margin-right: 12px;
    transition: all 0.2s ease;
    flex-shrink: 0;
}

/* 4. Active (Selected) state styling */
section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
    background: rgba(124, 58, 237, 0.08) !important;
    border-color: rgba(124, 58, 237, 0.15) !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"]::before {
    background: #3B82F6 !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 0 8px rgba(59, 130, 246, 0.6);
    transform: scale(1.2);
    display: inline-block !important; /* Always show the dot if checked */
}

/* 5. Hover effects for functional links */
section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-checked="true"]):hover {
    background: rgba(255, 255, 255, 0.03) !important;
    transform: translateX(3px);
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-checked="true"]):hover::before {
    border-color: #94A3B8 !important;
}

/* 6. Base Style for label text */
section[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    margin: 0 !important;
    font-size: 0.88rem !important;
    transition: color 0.2s ease !important;
}







/* ── Sidebar radio group spacing ─────────────── */
.stRadio > div { gap: 0 !important; }
.stRadio > div > div { gap: 0 !important; }
.stRadio [role="radiogroup"] { gap: 0 !important; }

/* ── Sidebar scrollbar ───────────────────────── */
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: transparent; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: rgba(96,165,250,0.2); border-radius: 4px; }


/* ── Alerts ───────────────────────────────── */
.stAlert { border-radius:10px !important; background:rgba(30,41,59,.7) !important; backdrop-filter:blur(10px) !important; border:none !important; border-left:4px solid #3B82F6 !important; }

/* ── Dataframes ───────────────────────────── */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,.05); }

/* ── File Uploader ────────────────────────── */
[data-testid="stFileUploadDropzone"] { background:rgba(30,41,59,.5); border:2px dashed rgba(255,255,255,.15); border-radius:14px; transition:all .3s; }
[data-testid="stFileUploadDropzone"]:hover { background:rgba(59,130,246,.05); border-color:#3B82F6; }

/* ── Metrics ──────────────────────────────── */
[data-testid="stMetricValue"] { font-size:2rem; font-weight:800; color:#F3F4F6; }
[data-testid="stMetricLabel"] { font-size:.9rem; color:#94A3B8; }

/* ── Footer ───────────────────────────────── */
.footer-container {
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding:2.5rem 0 2rem; margin-top:4rem;
    border-top:1px solid transparent;
    border-image:linear-gradient(90deg, transparent, rgba(167,139,250,.2), rgba(96,165,250,.2), transparent) 1;
    color:#64748B; font-size:.82rem; letter-spacing:.3px;
    position: relative;
}
.footer-container::before {
    content:''; position:absolute; top:-1px; left:20%; width:60%; height:1px;
    background:linear-gradient(90deg, transparent, rgba(167,139,250,.3), rgba(96,165,250,.3), transparent);
    filter: blur(1px);
}
.footer-container a { color:#60A5FA; text-decoration:none; font-weight:500; transition: color .2s; }
.footer-container a:hover { color:#A78BFA; }

/* ── Section Title with gradient underline ── */
.section-title {
    font-size: 1.5rem; font-weight: 700; color: #F1F5F9;
    margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 2px solid transparent;
    border-image: linear-gradient(90deg,#A78BFA,#60A5FA,#22D3EE) 1;
    position: relative;
}
</style>
""", unsafe_allow_html=True)



# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'system' not in st.session_state:
    st.session_state.system = None
if 'student_details_cache' not in st.session_state:
    st.session_state.student_details_cache = {}
if 'active_page' not in st.session_state:
    st.session_state.active_page = "🏠 Welcome"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


# ------------------------------
# Core Student Records System Class (SQL wrapper)
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
# Plotting functions (using Plotly for interactivity)
# ------------------------------
def plot_grades_by_course(course_history):
    """Bar chart of grades by course"""
    fig = px.bar(course_history.sort_values('grade', ascending=False),
                 x='course_code', y='grade', color='grade',
                 color_continuous_scale='Blues', title='Grades by Course',
                 labels={'grade': 'Grade', 'course_code': 'Course'})
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    return fig

def plot_attendance_by_course(course_history):
    """Bar chart of attendance by course"""
    course_history = course_history.copy()
    course_history['attendance_pct'] = course_history['attendance'] * 100
    fig = px.bar(course_history.sort_values('attendance', ascending=False),
                 x='course_code', y='attendance_pct', color='attendance_pct',
                 color_continuous_scale='Reds', title='Attendance by Course',
                 labels={'attendance_pct': 'Attendance (%)', 'course_code': 'Course'})
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    return fig

def plot_grade_distribution(course_history):
    """Histogram of grades"""
    fig = px.histogram(course_history, x='grade', nbins=10,
                       title='Grade Distribution',
                       labels={'grade': 'Grade', 'count': 'Frequency'},
                       color_discrete_sequence=['lightgreen'])
    fig.add_vline(x=course_history['grade'].mean(), line_dash="dash",
                  line_color="red", annotation_text=f"Mean: {course_history['grade'].mean():.2f}")
    return fig

def plot_semester_trend(course_history):
    """Semester-wise performance trend (dual axis)"""
    semester_data = course_history.groupby(['year', 'semester']).agg({
        'grade': 'mean',
        'attendance': 'mean'
    }).reset_index()
    semester_data['term'] = semester_data['semester'] + ' ' + semester_data['year'].astype(str)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=semester_data['term'], y=semester_data['grade'],
                   mode='lines+markers', name='Grade', line=dict(color='blue')),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=semester_data['term'], y=semester_data['attendance']*100,
                   mode='lines+markers', name='Attendance (%)', line=dict(color='red')),
        secondary_y=True
    )
    fig.update_layout(title='Semester-wise Performance Trend', xaxis_title='Semester')
    fig.update_yaxes(title_text='Grade', secondary_y=False)
    fig.update_yaxes(title_text='Attendance (%)', secondary_y=True)
    return fig

def plot_grade_vs_attendance(course_history):
    """Scatter plot: grade vs attendance"""
    fig = px.scatter(course_history, x='grade', y='attendance', size='credits',
                     color='credits', hover_name='course_code',
                     title='Grade vs Attendance Correlation',
                     labels={'grade': 'Grade', 'attendance': 'Attendance', 'credits': 'Credits'})
    corr = course_history['grade'].corr(course_history['attendance'])
    fig.add_annotation(x=0.05, y=0.95, xref='paper', yref='paper',
                       text=f'Correlation: {corr:.2f}', showarrow=False,
                       bgcolor='white', bordercolor='black', borderwidth=1)
    return fig

def plot_performance_by_level(course_history):
    """Grouped bar chart for performance by course level"""
    course_history['course_level'] = course_history['course_code'].str.extract(r'(\d+)').astype(int) // 100
    level_data = course_history.groupby('course_level').agg({
        'grade': 'mean',
        'attendance': 'mean'
    }).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=level_data['course_level'], y=level_data['grade'],
                         name='Grade', marker_color='#60A5FA', yaxis='y'))
    fig.add_trace(go.Bar(x=level_data['course_level'], y=level_data['attendance']*100,
                         name='Attendance (%)', marker_color='#A78BFA', yaxis='y2'))

    fig.update_layout(
        title='Performance by Course Level',
        xaxis=dict(title='Course Level', tickmode='array',
                   tickvals=level_data['course_level'],
                   ticktext=[f'Level {int(l)}' for l in level_data['course_level']]),
        yaxis=dict(title='Grade', side='left', range=[0, 4]),
        yaxis2=dict(title='Attendance (%)', side='right', range=[0, 100], overlaying='y', tickmode='sync'),
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F3F4F6')
    )
    return fig

def plot_credit_distribution(course_history):
    """Pie chart of credits by course level"""
    course_history['course_level'] = course_history['course_code'].str.extract(r'(\d+)').astype(int) // 100
    credit_totals = course_history.groupby('course_level')['credits'].sum().reset_index()
    credit_totals['course_level'] = 'Level ' + credit_totals['course_level'].astype(str)
    fig = px.pie(credit_totals, values='credits', names='course_level',
                 title='Credit Distribution by Course Level', hole=0.3)
    return fig

def plot_progression(course_history):
    """Line charts for progression over time"""
    course_history = course_history.sort_values(['year', 'semester'])
    course_history['term_sequence'] = range(len(course_history))
    course_history['cumulative_gpa'] = course_history['grade'].expanding().mean()
    course_history['cumulative_credits'] = course_history['credits'].cumsum()

    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Grade Progression', 'Attendance Progression',
                                        'Cumulative GPA', 'Cumulative Credits'))

    fig.add_trace(go.Scatter(x=course_history['term_sequence'], y=course_history['grade'],
                             mode='lines+markers', name='Grade'), row=1, col=1)
    fig.add_trace(go.Scatter(x=course_history['term_sequence'], y=course_history['attendance']*100,
                             mode='lines+markers', name='Attendance %'), row=1, col=2)
    fig.add_trace(go.Scatter(x=course_history['term_sequence'], y=course_history['cumulative_gpa'],
                             mode='lines+markers', name='Cumulative GPA'), row=2, col=1)
    fig.add_trace(go.Scatter(x=course_history['term_sequence'], y=course_history['cumulative_credits'],
                             mode='lines+markers', name='Cumulative Credits'), row=2, col=2)

    fig.update_xaxes(title_text='Course Sequence', row=1, col=1)
    fig.update_xaxes(title_text='Course Sequence', row=1, col=2)
    fig.update_xaxes(title_text='Course Sequence', row=2, col=1)
    fig.update_xaxes(title_text='Course Sequence', row=2, col=2)
    fig.update_yaxes(title_text='Grade', row=1, col=1)
    fig.update_yaxes(title_text='Attendance (%)', row=1, col=2)
    fig.update_yaxes(title_text='Cumulative GPA', row=2, col=1)
    fig.update_yaxes(title_text='Cumulative Credits', row=2, col=2)

    fig.update_layout(height=700, showlegend=False, title_text='Progression Over Time',
                      paper_bgcolor='rgba(0,0,0,0)', 
                      plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='#F3F4F6'),
                      title_font=dict(size=16, color='#60A5FA'))
    return fig


# ─── Helper: letter grade ──────────────────────────────────────────────────────
def letter_grade(gpa):
    if gpa >= 3.7: return 'A+'
    if gpa >= 3.3: return 'A'
    if gpa >= 3.0: return 'A-'
    if gpa >= 2.7: return 'B+'
    if gpa >= 2.3: return 'B'
    if gpa >= 2.0: return 'B-'
    if gpa >= 1.7: return 'C+'
    if gpa >= 1.3: return 'C'
    if gpa >= 1.0: return 'C-'
    return 'F'

def transparent_layout(fig):
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='#F3F4F6'))
    return fig

# ─── Page: Landing / Welcome ───────────────────────────────────────────────────
def render_landing(system):
    # ── CSS block (separate from HTML to avoid Streamlit sanitizer issues) ────
    st.markdown("""
    <style>
    .hero-wrap {
        text-align:center; padding:3.5rem 1rem 2.8rem;
        background:linear-gradient(160deg,rgba(10,15,30,0) 0%,rgba(99,102,241,.07) 50%,rgba(10,15,30,0) 100%);
        border-radius:24px; border:1px solid rgba(99,102,241,.14);
        margin-bottom:2rem; position:relative; overflow:hidden;
    }
    .hero-wrap::before {
        content:''; position:absolute; inset:0;
        background:radial-gradient(ellipse 70% 55% at 50% 0%,rgba(99,102,241,.13),transparent);
        pointer-events:none;
    }
    .hero-badge {
        display:inline-flex; align-items:center; gap:6px;
        background:rgba(99,102,241,.13); border:1px solid rgba(99,102,241,.32);
        color:#A5B4FC; font-size:.73rem; font-weight:700;
        padding:4px 16px; border-radius:999px; letter-spacing:1.2px;
        text-transform:uppercase; margin-bottom:1.3rem;
    }
    .hero-headline {
        font-size:3.4rem; font-weight:900; line-height:1.1;
        letter-spacing:-2px; margin:0 0 1rem;
        background:linear-gradient(120deg,#E2E8F0 0%,#A78BFA 38%,#60A5FA 68%,#34D399 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }
    .hero-subline {
        font-size:1.05rem; color:#64748B; max-width:560px;
        margin:0 auto 2rem; line-height:1.75; font-weight:400;
    }
    .hero-subline strong { color:#94A3B8; font-weight:600; }
    .stat-strip {
        display:flex; border:1px solid rgba(255,255,255,.06);
        border-radius:14px; overflow:hidden; margin:2.5rem 0 0;
        background:rgba(15,23,42,.65); backdrop-filter:blur(12px);
    }
    .stat-item {
        flex:1; padding:1.15rem .7rem;
        border-right:1px solid rgba(255,255,255,.05); text-align:center;
    }
    .stat-item:last-child { border-right:none; }
    .stat-num {
        font-size:1.65rem; font-weight:800;
        background:linear-gradient(135deg,#A78BFA,#60A5FA);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    }
    .stat-label { font-size:.68rem; color:#475569; font-weight:600;
                  text-transform:uppercase; letter-spacing:.9px; margin-top:3px; }
    .feat-item {
        background:rgba(15,23,42,.72); border:1px solid rgba(255,255,255,.06);
        border-radius:16px; padding:1.4rem 1.2rem;
        transition:transform .22s ease, box-shadow .22s, border-color .22s;
    }
    .feat-item:hover { transform:translateY(-5px); border-color:rgba(99,102,241,.32);
                       box-shadow:0 12px 32px rgba(0,0,0,.38); }
    .feat-icon-wrap {
        width:46px; height:46px; border-radius:12px;
        display:flex; align-items:center; justify-content:center;
        font-size:1.35rem; margin-bottom:.85rem;
    }
    .feat-name { font-weight:700; font-size:.94rem; color:#E2E8F0; margin-bottom:.3rem; }
    .feat-desc { font-size:.79rem; color:#475569; line-height:1.55; }
    .cta-wrap {
        background:linear-gradient(135deg,rgba(30,41,59,.82),rgba(15,23,42,.92));
        border:1px solid rgba(255,255,255,.07); border-radius:20px;
        padding:2rem 2rem 1.5rem; margin:1.5rem 0;
    }
    .cta-title { font-size:1.3rem; font-weight:800; color:#E2E8F0; margin-bottom:.3rem; }
    .cta-sub { font-size:.87rem; color:#64748B; margin:0; }
    .trust-strip {
        display:flex; justify-content:center; gap:1.8rem;
        margin:2rem 0 .5rem; flex-wrap:wrap;
    }
    .trust-item { color:#334155; font-size:.8rem; font-weight:600; }

    /* ── 3D Floating Geometric Shapes (Hero) ────────────── */
    .hero-scene-3d { position:absolute; inset:0; pointer-events:none; perspective:800px; overflow:hidden; z-index:0; }
    /* ── Shape 1: Orbital Data Rings ── */
    .hero-shape-orbital { position:absolute; top:12%; left:8%; width:80px; height:80px; transform-style:preserve-3d; animation:heroOrbitalFloat 14s ease-in-out infinite, heroOrbitalSpin 20s linear infinite; }
    .hero-shape-orbital .ring { position:absolute; width:100%; height:100%; border-radius:50%; opacity:0.8; border: 2px solid rgba(167,139,250,.3); }
    .hero-shape-orbital .r1 { transform: rotateX(65deg) rotateY(0deg); border-color: rgba(96,165,250,.4); }
    .hero-shape-orbital .r2 { transform: rotateX(65deg) rotateY(60deg); border-color: rgba(167,139,250,.4); }
    .hero-shape-orbital .r3 { transform: rotateX(65deg) rotateY(120deg); border-color: rgba(52,211,153,.4); }
    .hero-shape-orbital .core { position:absolute; top:50%; left:50%; width:16px; height:16px; background:radial-gradient(circle, #60A5FA, transparent); border-radius:50%; transform:translate(-50%,-50%); box-shadow:0 0 15px rgba(96,165,250,.6); }
    @keyframes heroOrbitalSpin { 0%{transform:rotateX(0) rotateY(0) rotateZ(0);} 100%{transform:rotateX(360deg) rotateY(360deg) rotateZ(180deg);} }
    @keyframes heroOrbitalFloat { 0%,100%{top:12%;} 50%{top:8%;} }

    .hero-shape-ring { position:absolute; bottom:15%; right:10%; width:90px; height:90px; border:1.5px solid rgba(167,139,250,.2); border-radius:50%; transform-style:preserve-3d; animation:heroRingOrb 10s linear infinite; box-shadow:0 0 20px rgba(167,139,250,.1); }
    .hero-shape-ring::after { content:''; position:absolute; top:-4px; left:50%; width:8px; height:8px; border-radius:50%; transform:translateX(-50%); background:#A78BFA; box-shadow:0 0 15px #A78BFA,0 0 30px rgba(167,139,250,.6); }
    @keyframes heroRingOrb { 0%{transform:rotateX(70deg) rotateZ(0);} 100%{transform:rotateX(70deg) rotateZ(360deg);} }

    .hero-shape-diamond { position:absolute; top:20%; right:22%; width:40px; height:40px; transform-style:preserve-3d; animation:heroDiamSpin 16s linear infinite,heroDiamFloat 12s ease-in-out infinite; }
    .hero-shape-diamond::before,.hero-shape-diamond::after { content:''; position:absolute; width:0; height:0; left:50%; transform:translateX(-50%); border-left:20px solid transparent; border-right:20px solid transparent; }
    .hero-shape-diamond::before { top:-2px; border-bottom:30px solid rgba(52,211,153,.15); filter:drop-shadow(0 0 10px rgba(52,211,153,.3)); }
    .hero-shape-diamond::after { bottom:-2px; border-top:30px solid rgba(96,165,250,.15); filter:drop-shadow(0 0 10px rgba(96,165,250,.3)); }
    @keyframes heroDiamSpin { 0%{transform:rotateY(0) rotateZ(0);} 100%{transform:rotateY(360deg) rotateZ(360deg);} }
    @keyframes heroDiamFloat { 0%,100%{top:20%;} 50%{top:16%;} }

    .hero-shape-pyr { position:absolute; bottom:25%; left:15%; width:45px; height:45px; transform-style:preserve-3d; animation:heroPyrSpin 14s linear infinite,heroPyrFloat 9s ease-in-out infinite; }
    .hero-pyr-face { position:absolute; width:0; height:0; border-left:22px solid transparent; border-right:22px solid transparent; border-bottom:40px solid rgba(96,165,250,.12); transform-origin:bottom center; }
    .hero-pyr-f1 {transform:rotateY(0deg) rotateX(30deg) translateZ(0);}
    .hero-pyr-f2 {transform:rotateY(90deg) rotateX(30deg) translateZ(0);}
    .hero-pyr-f3 {transform:rotateY(180deg) rotateX(30deg) translateZ(0);}
    .hero-pyr-f4 {transform:rotateY(270deg) rotateX(30deg) translateZ(0);}
    @keyframes heroPyrSpin { 0%{transform:rotateY(0);} 100%{transform:rotateY(360deg);} }
    @keyframes heroPyrFloat { 0%,100%{bottom:25%;} 50%{bottom:29%;} }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero HTML (no HTML comments — they break Streamlit's sanitizer) ───────
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-scene-3d">
            <div class="hero-shape-orbital"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
            <div class="hero-shape-ring"></div>
            <div class="hero-shape-diamond"></div>
            <div class="hero-shape-pyr"><div class="hero-pyr-face hero-pyr-f1"></div><div class="hero-pyr-face hero-pyr-f2"></div><div class="hero-pyr-face hero-pyr-f3"></div><div class="hero-pyr-face hero-pyr-f4"></div></div>
        </div>
        <div class="hero-badge">✦ School &amp; College Edition</div>
        <div class="hero-headline">Academic Analytics<br>Made Effortless</div>
        <div class="hero-subline">
            A <strong>complete intelligence platform</strong> for institutions — track grades,
            attendance, at-risk students, top performers, transcripts &amp; more.
            All in one place. No code needed.
        </div>
        <div class="stat-strip">
            <div class="stat-item"><div class="stat-num">15+</div><div class="stat-label">Analytics Pages</div></div>
            <div class="stat-item"><div class="stat-num">1500</div><div class="stat-label">Demo Students</div></div>
            <div class="stat-item"><div class="stat-num">Live</div><div class="stat-label">Charts &amp; Insights</div></div>
            <div class="stat-item"><div class="stat-num">PDF</div><div class="stat-label">Transcript Export</div></div>
            <div class="stat-item"><div class="stat-num">Zero</div><div class="stat-label">Coding Required</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature Grid ─────────────────────────────────────────────────────────
    features = [
        ("📊","#3B82F6","Dashboard",        "Live KPIs — GPA, attendance & at-risk count at a glance"),
        ("🚨","#EF4444","At-Risk Alerts",   "Flag students with low GPA or poor attendance early"),
        ("🏆","#F59E0B","Top Performers",   "Honor roll leaderboard & perfect attendance awards"),
        ("🏫","#8B5CF6","Dept Overview",    "Compare departments on GPA, pass rate & enrollment"),
        ("📋","#10B981","Attendance",        "Dept-wise charts, trends & critical absentee list"),
        ("🎯","#EC4899","Pass / Fail",      "Course-level pass/fail counts with alert thresholds"),
        ("📊","#06B6D4","Batch Compare",    "Side-by-side department or semester comparison"),
        ("🔔","#F97316","Improvement Track","See who improved or declined semester-over-semester"),
        ("📄","#6366F1","Transcripts + PDF","Letter graded, styled PDF or CSV transcript download"),
    ]
    cols = st.columns(3)
    for i, (icon, color, title, desc) in enumerate(features):
        light = color + "22"
        cols[i % 3].markdown(f"""
        <div class="feat-item" style="margin-bottom:1rem;">
            <div class="feat-icon-wrap" style="background:{light}; border:1px solid {color}44;">
                <span>{icon}</span>
            </div>
            <div class="feat-name">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Get Started Section ───────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-wrap">
        <div class="cta-title">🚀 Get Started in Seconds</div>
        <div class="cta-sub">Load the built-in demo dataset or upload your own CSV to explore all features.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(59,130,246,.12),rgba(99,102,241,.06));
                    border:1px solid rgba(59,130,246,.25);border-radius:14px;padding:1.3rem 1.2rem .8rem;">
            <div style="font-size:1.5rem;margin-bottom:.3rem;">🗂</div>
            <div style="font-weight:700;color:#E2E8F0;font-size:.95rem;margin-bottom:.2rem;">Try Demo Dataset</div>
            <div style="color:#475569;font-size:.8rem;margin-bottom:.8rem;">
                1,500 pre-generated students across multiple departments.
                Perfect for exploring all 15 features instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶  Load 1,500 Demo Students", use_container_width=True):
            with st.spinner("Generating dataset…"):
                system.load_data()
                st.session_state.data = system.data
            st.success("✅ Demo data loaded! Click **📊 Dashboard** in the sidebar.")

    with c2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(16,185,129,.1),rgba(52,211,153,.04));
                    border:1px solid rgba(16,185,129,.2);border-radius:14px;padding:1.3rem 1.2rem .8rem;">
            <div style="font-size:1.5rem;margin-bottom:.3rem;">📂</div>
            <div style="font-weight:700;color:#E2E8F0;font-size:.95rem;margin-bottom:.2rem;">Upload Your CSV</div>
            <div style="color:#475569;font-size:.79rem;margin-bottom:.5rem;">
                Required columns:
                <code style="color:#34D399;background:rgba(52,211,153,.1);padding:1px 5px;border-radius:4px;font-size:.75rem;">
                    student_id, major, grade, attendance, credits, semester, year
                </code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader("", type="csv", label_visibility="collapsed")
        if uploaded:
            with st.spinner("Loading your data…"):
                ok = system.load_data(uploaded)
            if ok:
                st.session_state.data = system.data
                st.success("✅ Loaded! Click **📊 Dashboard** to explore.")
            else:
                st.error("❌ Failed. Check your column names.")

    # ── Trust Strip ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="trust-strip">
        <div class="trust-item">✅&nbsp; No database needed</div>
        <div class="trust-item">✅&nbsp; CSV upload support</div>
        <div class="trust-item">✅&nbsp; PDF transcript export</div>
        <div class="trust-item">✅&nbsp; 100% offline capable</div>
        <div class="trust-item">✅&nbsp; School &amp; college ready</div>
    </div>
    """, unsafe_allow_html=True)

def render_at_risk(data):
    st.markdown('<p class="section-title">🚨 At-Risk Students</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8; margin-bottom:1.5rem;">Students flagged for low GPA (< 2.0) or low attendance (< 75%)</p>', unsafe_allow_html=True)
    
    if data is None or data.empty or 'student_id' not in data.columns:
        st.warning("⚠️ No data available. Please load student records from the Welcome page.")
        return

    student_agg = data.groupby(['student_id','first_name','last_name','major']).agg(
        cgpa=('grade','mean'), attendance=('attendance','mean')
    ).reset_index()
    student_agg['cgpa']       = student_agg['cgpa'].round(2)
    student_agg['attendance'] = student_agg['attendance'].round(3)

    low_gpa  = student_agg['cgpa'] < 2.0
    low_att  = student_agg['attendance'] < 0.75
    at_risk  = student_agg[low_gpa | low_att].copy()
    at_risk['Risk Reason'] = ''
    at_risk.loc[low_gpa & ~low_att, 'Risk Reason'] = 'Low GPA'
    at_risk.loc[~low_gpa & low_att, 'Risk Reason'] = 'Low Attendance'
    at_risk.loc[low_gpa & low_att,  'Risk Reason'] = 'Low GPA & Attendance'
    at_risk = at_risk.sort_values('cgpa')

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card danger-card"><h3>Total At Risk</h3><p>{len(at_risk)}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card warning-card"><h3>Low GPA Only</h3><p>{(low_gpa & ~low_att).sum()}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card danger-card"><h3>Both Issues</h3><p>{(low_gpa & low_att).sum()}</p></div>', unsafe_allow_html=True)
    st.write("")

    f1, f2 = st.columns(2)
    reason_filter = f1.selectbox("Filter by Reason", ["All", "Low GPA", "Low Attendance", "Low GPA & Attendance"])
    major_filter  = f2.selectbox("Filter by Major",  ["All"] + sorted(data['major'].unique().tolist()))
    if reason_filter != "All": at_risk = at_risk[at_risk['Risk Reason'] == reason_filter]
    if major_filter  != "All": at_risk = at_risk[at_risk['major'] == major_filter]

    display = at_risk.rename(columns={'student_id':'ID','first_name':'First','last_name':'Last','major':'Major','cgpa':'GPA','attendance':'Attendance'})
    display['Attendance'] = (display['Attendance']*100).round(1).astype(str) + '%'
    st.dataframe(display[['ID','First','Last','Major','GPA','Attendance','Risk Reason']], use_container_width=True)
    st.download_button("⬇ Download At-Risk Report (CSV)", at_risk.to_csv(index=False), "at_risk_students.csv", "text/csv")

    fig = px.bar(at_risk.groupby('major').size().reset_index(name='count'),
                 x='major', y='count', title='At-Risk Students by Department',
                 color='count', color_continuous_scale='Reds')
    st.plotly_chart(transparent_layout(fig), use_container_width=True)

# ─── Page: Top Performers ──────────────────────────────────────────────────────
def render_top_performers(data):
    st.markdown('<p class="section-title">🏆 Top Performers</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8; margin-bottom:1.5rem;">Students maintaining a CGPA of 3.5 or higher</p>', unsafe_allow_html=True)

    if data is None or data.empty or 'student_id' not in data.columns:
        st.warning("⚠️ No data available. Please load student records from the Welcome page.")
        return

    student_agg = data.groupby(['student_id','first_name','last_name','major']).agg(
        cgpa=('grade','mean'), attendance=('attendance','mean'), credits=('credits','sum')
    ).reset_index()
    student_agg['cgpa']       = student_agg['cgpa'].round(2)
    student_agg['attendance'] = student_agg['attendance'].round(3)

    honor_roll  = student_agg[student_agg['cgpa'] >= 3.5].sort_values('cgpa', ascending=False).reset_index(drop=True)
    perfect_att = student_agg[student_agg['attendance'] >= 0.97].sort_values('attendance', ascending=False).reset_index(drop=True)
    both        = student_agg[(student_agg['cgpa'] >= 3.5) & (student_agg['attendance'] >= 0.97)]

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card success-card"><h3>Honor Roll</h3><p>{len(honor_roll)}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card success-card"><h3>Perfect Attendance</h3><p>{len(perfect_att)}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card info-card"><h3>Both Honours</h3><p>{len(both)}</p></div>', unsafe_allow_html=True)
    st.write("")

    tab1, tab2 = st.tabs(["🎖 Honor Roll", "📅 Perfect Attendance"])
    with tab1:
        honor_roll['Rank'] = honor_roll.index + 1
        honor_roll['Letter'] = honor_roll['cgpa'].apply(letter_grade)
        d = honor_roll.rename(columns={'student_id':'ID','first_name':'First','last_name':'Last','major':'Major','cgpa':'GPA'})
        st.dataframe(d[['Rank','ID','First','Last','Major','GPA','Letter']], use_container_width=True)
    with tab2:
        perfect_att['Rank'] = perfect_att.index + 1
        perfect_att['Att%'] = (perfect_att['attendance']*100).round(1).astype(str) + '%'
        d = perfect_att.rename(columns={'student_id':'ID','first_name':'First','last_name':'Last','major':'Major','cgpa':'GPA'})
        st.dataframe(d[['Rank','ID','First','Last','Major','GPA','Att%']], use_container_width=True)

    fig = px.bar(honor_roll.head(10), x='cgpa',
                 y=honor_roll.head(10)['first_name']+' '+honor_roll.head(10)['last_name'],
                 orientation='h', title='Top 10 Students by GPA',
                 color='cgpa', color_continuous_scale='greens')
    fig.update_yaxes(title='Student')
    st.plotly_chart(transparent_layout(fig), use_container_width=True)

# ─── Page: Attendance Overview ─────────────────────────────────────────────────
def render_attendance(data):
    st.markdown('<p class="section-title">📋 Attendance Overview</p>', unsafe_allow_html=True)

    student_agg = data.groupby(['student_id','first_name','last_name','major']).agg(
        attendance=('attendance','mean')
    ).reset_index()
    overall_avg = student_agg['attendance'].mean()
    critical    = student_agg[student_agg['attendance'] < 0.60]
    good        = student_agg[student_agg['attendance'] >= 0.90]

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card info-card"><h3>Avg Attendance</h3><p>{overall_avg*100:.1f}%</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card danger-card"><h3>Critical (&lt;60%)</h3><p>{len(critical)}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card success-card"><h3>Good (≥90%)</h3><p>{len(good)}</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card warning-card"><h3>Total Students</h3><p>{student_agg["student_id"].nunique()}</p></div>', unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        dept_avg = data.groupby('major')['attendance'].mean().reset_index().sort_values('attendance', ascending=True)
        dept_avg['attendance_pct'] = (dept_avg['attendance']*100).round(1)
        fig = px.bar(dept_avg, x='attendance_pct', y='major', orientation='h',
                     title='Avg Attendance by Department', color='attendance_pct',
                     color_continuous_scale='RdYlGn', range_color=[70,100])
        fig.update_xaxes(title='Attendance %')
        st.plotly_chart(transparent_layout(fig), use_container_width=True)
    with col2:
        fig = px.histogram(student_agg, x='attendance', nbins=20,
                           title='Student Attendance Distribution',
                           color_discrete_sequence=['#60A5FA'])
        fig.update_xaxes(tickformat='.0%')
        st.plotly_chart(transparent_layout(fig), use_container_width=True)

    st.subheader("🔴 Critical Attendance List (< 60%)")
    if critical.empty:
        st.success("No students with critical attendance!")
    else:
        d = critical.rename(columns={'student_id':'ID','first_name':'First','last_name':'Last','major':'Major'})
        d = d.copy()
        d['Attendance'] = (d['attendance']*100).round(1).astype(str) + '%'
        st.dataframe(d[['ID','First','Last','Major','Attendance']], use_container_width=True)
        st.download_button("⬇ Download Critical List (CSV)", critical.to_csv(index=False), "critical_attendance.csv", "text/csv")

# ─── Streamlit UI ──────────────────────────────────────────────────────────────


# ─── Page: Department Overview ─────────────────────────────────────────────────
def render_department_overview(data):
    st.markdown('<p class="section-title">🏫 Department Overview</p>', unsafe_allow_html=True)
    st.caption("Department-level GPA, attendance, pass rate, and enrollment breakdown")

    dept = data.groupby(['major','student_id']).agg(cgpa=('grade','mean'), attendance=('attendance','mean')).reset_index()
    dept_summary = dept.groupby('major').agg(
        students=('student_id','nunique'),
        avg_gpa=('cgpa','mean'),
        avg_att=('attendance','mean')
    ).reset_index()
    dept_summary['pass_rate'] = dept.groupby('major').apply(lambda x: (x['cgpa'] >= 2.0).sum() / len(x) * 100).values
    dept_summary['avg_gpa']   = dept_summary['avg_gpa'].round(2)
    dept_summary['avg_att']   = (dept_summary['avg_att'] * 100).round(1)
    dept_summary['pass_rate'] = dept_summary['pass_rate'].round(1)
    dept_summary = dept_summary.sort_values('avg_gpa', ascending=False).reset_index(drop=True)
    dept_summary['Rank'] = dept_summary.index + 1

    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card info-card"><h3>Departments</h3><p>{len(dept_summary)}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card success-card"><h3>Best Dept GPA</h3><p>{dept_summary["avg_gpa"].max()}</p><div class="sub">{dept_summary.loc[dept_summary["avg_gpa"].idxmax(),"major"]}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card warning-card"><h3>Highest Enrollment</h3><p>{dept_summary["students"].max()}</p><div class="sub">{dept_summary.loc[dept_summary["students"].idxmax(),"major"]}</div></div>', unsafe_allow_html=True)
    st.write("")

    display = dept_summary.rename(columns={'major':'Department','students':'Students','avg_gpa':'Avg GPA','avg_att':'Avg Att%','pass_rate':'Pass Rate%'})
    st.dataframe(display[['Rank','Department','Students','Avg GPA','Avg Att%','Pass Rate%']], use_container_width=True)
    st.download_button("⬇ Download Department Report (CSV)", dept_summary.to_csv(index=False), "department_overview.csv", "text/csv")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(dept_summary.sort_values('avg_gpa'), x='avg_gpa', y='major', orientation='h',
                     title='Average GPA by Department', color='avg_gpa',
                     color_continuous_scale='Blues', range_color=[2,4])
        st.plotly_chart(transparent_layout(fig), use_container_width=True)
    with col2:
        fig = px.bar(dept_summary.sort_values('pass_rate'), x='pass_rate', y='major', orientation='h',
                     title='Pass Rate (%) by Department', color='pass_rate',
                     color_continuous_scale='RdYlGn', range_color=[60,100])
        st.plotly_chart(transparent_layout(fig), use_container_width=True)

    fig = px.scatter(dept_summary, x='avg_att', y='avg_gpa', size='students', color='major',
                     text='major', title='Attendance vs GPA by Department (bubble = enrollment)',
                     labels={'avg_att':'Avg Attendance%','avg_gpa':'Avg GPA'})
    fig.update_traces(textposition='top center')
    st.plotly_chart(transparent_layout(fig), use_container_width=True)


# ─── Page: Semester Report Card ────────────────────────────────────────────────
def render_semester_report(data, system):
    st.markdown('<p class="section-title">📅 Semester Report Card</p>', unsafe_allow_html=True)
    st.caption("Per-semester academic performance for individual students")

    sid = st.text_input("Enter Student ID or Name", key="semester_report_search", placeholder="e.g. 1042 or James Smith")
    if st.button("Generate Report Card", key="gen_report_card") and sid:
        student_details, course_history = system.get_student_details(sid)
        if student_details is not None and not student_details.empty:
            for _, student in student_details.iterrows():
                sc = course_history[course_history['student_id'] == student['student_id']].copy()
                sc['Letter']  = sc['grade'].apply(letter_grade)
                sc['Att%']    = (sc['attendance']*100).round(1)

                sem_table = sc.groupby(['year','semester']).agg(
                    gpa=('grade','mean'), att=('attendance','mean'),
                    credits=('credits','sum'), courses=('course_code','count')
                ).reset_index()
                sem_table['gpa']    = sem_table['gpa'].round(2)
                sem_table['att']    = (sem_table['att']*100).round(1)
                sem_table['Letter'] = sem_table['gpa'].apply(letter_grade)
                sem_table['Term']   = sem_table['semester'] + ' ' + sem_table['year'].astype(str)
                sem_table = sem_table.sort_values(['year','semester'])
                sem_table['Cumulative GPA'] = sem_table['gpa'].expanding().mean().round(2)

                st.markdown(f"""
                <div class="student-info">
                    <h3>📅 Semester Report Card</h3>
                    <strong>Name:</strong> {student['first_name']} {student['last_name']}&nbsp;
                    <strong>ID:</strong> {student['student_id']}<br>
                    <strong>Major:</strong> {student['major']}&nbsp;
                    <strong>Overall CGPA:</strong> {student['cgpa']:.2f}/4.0 ({letter_grade(student['cgpa'])})
                </div>""", unsafe_allow_html=True)

                display = sem_table.rename(columns={'gpa':'Sem GPA','att':'Att%','credits':'Credits','courses':'Courses'})
                st.dataframe(display[['Term','Courses','Credits','Sem GPA','Letter','Att%','Cumulative GPA']], use_container_width=True)

                fig = px.line(sem_table, x='Term', y='gpa', markers=True,
                              title='Semester-wise GPA Progression',
                              color_discrete_sequence=['#60A5FA'])
                fig.add_scatter(x=sem_table['Term'], y=sem_table['Cumulative GPA'],
                                mode='lines+markers', name='Cumulative GPA', line=dict(color='#34D399', dash='dash'))
                st.plotly_chart(transparent_layout(fig), use_container_width=True)

                col1, col2 = st.columns(2)
                col1.download_button("⬇ Download Report CSV", sem_table.to_csv(index=False),
                                     f"report_card_{student['student_id']}.csv", "text/csv")
        else:
            st.error("Student not found.")


# ─── Page: Class/Batch Comparison ──────────────────────────────────────────────
def render_batch_comparison(data):
    st.markdown('<p class="section-title">📊 Class / Batch Comparison</p>', unsafe_allow_html=True)
    st.caption("Compare two departments or two semesters side-by-side")

    tab1, tab2 = st.tabs(["🏫 Compare Departments", "📅 Compare Semesters"])

    with tab1:
        majors = sorted(data['major'].unique().tolist())
        c1, c2 = st.columns(2)
        dept_a = c1.selectbox("Department A", majors, index=0, key="dept_a")
        dept_b = c2.selectbox("Department B", majors, index=1, key="dept_b")

        if dept_a == dept_b:
            st.warning("Please select two different departments.")
        else:
            da = data[data['major'] == dept_a]
            db = data[data['major'] == dept_b]

            metrics = []
            for d, name in [(da, dept_a), (db, dept_b)]:
                stu = d.groupby('student_id').agg(cgpa=('grade','mean'), att=('attendance','mean')).reset_index()
                metrics.append({
                    'Dept': name,
                    'Students': stu['student_id'].nunique(),
                    'Avg GPA': round(stu['cgpa'].mean(), 2),
                    'Avg Att%': round(stu['att'].mean() * 100, 1),
                    'Pass Rate%': round((stu['cgpa'] >= 2.0).mean() * 100, 1),
                    'Top Performers': int((stu['cgpa'] >= 3.5).sum()),
                    'At Risk': int(((stu['cgpa'] < 2.0) | (stu['att'] < 0.75)).sum()),
                })
            df_m = pd.DataFrame(metrics).set_index('Dept').T
            st.dataframe(df_m, use_container_width=True)

            m1,m2 = st.columns(2)
            fig = px.histogram(data[data['major'].isin([dept_a, dept_b])],
                               x='grade', color='major', barmode='overlay', opacity=0.7,
                               title='GPA Distribution Comparison',
                               color_discrete_sequence=['#60A5FA','#F472B6'])
            m1.plotly_chart(transparent_layout(fig), use_container_width=True)
            fig = px.box(data[data['major'].isin([dept_a, dept_b])],
                         x='major', y='grade', color='major',
                         title='GPA Spread Comparison',
                         color_discrete_sequence=['#60A5FA','#F472B6'])
            m2.plotly_chart(transparent_layout(fig), use_container_width=True)

    with tab2:
        years = sorted(data['year'].unique().tolist())
        semester_options = sorted(data[['year','semester']].drop_duplicates().apply(lambda r: f"{r['semester']} {r['year']}", axis=1).tolist())
        sc1,sc2 = st.columns(2)
        sem_a = sc1.selectbox("Semester A", semester_options, index=0, key="sem_a")
        sem_b = sc2.selectbox("Semester B", semester_options, index=min(1, len(semester_options)-1), key="sem_b")

        def parse_sem(s):
            parts = s.split()
            return parts[0], int(parts[1])

        sem_a_name, sem_a_year = parse_sem(sem_a)
        sem_b_name, sem_b_year = parse_sem(sem_b)
        da = data[(data['semester']==sem_a_name) & (data['year']==sem_a_year)]
        db = data[(data['semester']==sem_b_name) & (data['year']==sem_b_year)]

        metrics = []
        for d, label in [(da, sem_a), (db, sem_b)]:
            metrics.append({
                'Semester': label,
                'Records': len(d),
                'Avg GPA': round(d['grade'].mean(), 2),
                'Avg Att%': round(d['attendance'].mean() * 100, 1),
                'Pass Rate%': round((d['grade'] >= 2.0).mean() * 100, 1),
            })
        st.dataframe(pd.DataFrame(metrics).set_index('Semester').T, use_container_width=True)

        combined = pd.concat([da.assign(Term=sem_a), db.assign(Term=sem_b)])
        fig = px.box(combined, x='Term', y='grade', color='Term',
                     title='Grade Distribution Comparison',
                     color_discrete_sequence=['#A78BFA','#34D399'])
        st.plotly_chart(transparent_layout(fig), use_container_width=True)


# ─── Page: Pass/Fail Summary ───────────────────────────────────────────────────
def render_pass_fail(data):
    st.markdown('<p class="section-title">🎯 Pass / Fail Summary</p>', unsafe_allow_html=True)
    st.caption("Course-level pass/fail breakdown. Pass = GPA ≥ 2.0")

    data = data.copy()
    data['Status'] = data['grade'].apply(lambda g: 'Pass' if g >= 2.0 else 'Fail')

    course_pf = data.groupby('course_code').agg(
        total=('student_id','count'),
        passed=('Status', lambda x: (x=='Pass').sum()),
        failed=('Status', lambda x: (x=='Fail').sum()),
        avg_grade=('grade','mean')
    ).reset_index()
    course_pf['pass_rate'] = (course_pf['passed'] / course_pf['total'] * 100).round(1)
    course_pf['avg_grade'] = course_pf['avg_grade'].round(2)
    course_pf = course_pf.sort_values('pass_rate', ascending=False)

    c1,c2,c3,c4 = st.columns(4)
    total_pass = (data['Status']=='Pass').sum()
    total_fail = (data['Status']=='Fail').sum()
    c1.markdown(f'<div class="metric-card info-card"><h3>Total Records</h3><p>{len(data)}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card success-card"><h3>Pass</h3><p>{total_pass}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card danger-card"><h3>Fail</h3><p>{total_fail}</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card warning-card"><h3>Overall Pass Rate</h3><p>{total_pass/len(data)*100:.1f}%</p></div>', unsafe_allow_html=True)
    st.write("")

    # Filters
    f1, f2 = st.columns(2)
    major_filter = f1.selectbox("Filter by Department", ["All"] + sorted(data['major'].unique().tolist()), key="pf_major")
    threshold    = f2.slider("Highlight courses with pass rate below (%)", 50, 90, 70, key="pf_thresh")

    filtered_data = data if major_filter == "All" else data[data['major'] == major_filter]
    cpf = filtered_data.groupby('course_code').agg(
        total=('student_id','count'),
        passed=('Status', lambda x: (x=='Pass').sum()),
        failed=('Status', lambda x: (x=='Fail').sum()),
        avg_grade=('grade','mean')
    ).reset_index()
    cpf['pass_rate'] = (cpf['passed'] / cpf['total'] * 100).round(1)
    cpf['avg_grade'] = cpf['avg_grade'].round(2)
    cpf['⚠ Alert'] = cpf['pass_rate'].apply(lambda r: '🔴 Low' if r < threshold else '🟢 OK')
    cpf = cpf.sort_values('pass_rate', ascending=False)

    st.dataframe(cpf.rename(columns={'course_code':'Course','total':'Total','passed':'Passed',
                                      'failed':'Failed','avg_grade':'Avg Grade','pass_rate':'Pass Rate%'}),
                 use_container_width=True)
    st.download_button("⬇ Download Pass/Fail Report (CSV)", cpf.to_csv(index=False), "pass_fail_report.csv", "text/csv")

    col1, col2 = st.columns(2)
    with col1:
        low_pass = cpf[cpf['pass_rate'] < threshold].sort_values('pass_rate')
        if not low_pass.empty:
            fig = px.bar(low_pass, x='pass_rate', y='course_code', orientation='h',
                         title=f'Courses Below {threshold}% Pass Rate',
                         color='pass_rate', color_continuous_scale='Reds_r')
            st.plotly_chart(transparent_layout(fig), use_container_width=True)
        else:
            st.success(f"All courses have pass rate ≥ {threshold}%!")
    with col2:
        pie_data = pd.DataFrame({'Status':['Pass','Fail'],'Count':[total_pass,total_fail]})
        fig = px.pie(pie_data, values='Count', names='Status', title='Overall Pass/Fail Ratio',
                     color='Status', color_discrete_map={'Pass':'#10B981','Fail':'#EF4444'}, hole=0.4)
        st.plotly_chart(transparent_layout(fig), use_container_width=True)


# ─── Page: Improvement Tracking ────────────────────────────────────────────────
def render_improvement_tracking(data):
    st.markdown('<p class="section-title">🔔 Improvement Tracking</p>', unsafe_allow_html=True)
    st.caption("Students whose GPA improved or declined significantly semester-over-semester")

    data = data.copy()
    sem_order = data[['year','semester']].drop_duplicates().sort_values(['year','semester'])
    sem_order['term_rank'] = range(len(sem_order))
    data = data.merge(sem_order, on=['year','semester'])

    student_sem = data.groupby(['student_id','first_name','last_name','major','term_rank','semester','year']).agg(
        gpa=('grade','mean')
    ).reset_index().sort_values(['student_id','term_rank'])

    student_sem['prev_gpa'] = student_sem.groupby('student_id')['gpa'].shift(1)
    student_sem['delta']    = (student_sem['gpa'] - student_sem['prev_gpa']).round(2)
    student_sem = student_sem.dropna(subset=['delta'])
    student_sem['Trend'] = student_sem['delta'].apply(
        lambda d: '📈 Improved' if d >= 0.2 else ('📉 Declined' if d <= -0.2 else '➖ Stable'))

    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card success-card"><h3>Improved</h3><p>{(student_sem["delta"]>=0.2).sum()}</p><div class="sub">Δ ≥ +0.2 GPA</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card danger-card"><h3>Declined</h3><p>{(student_sem["delta"]<=-0.2).sum()}</p><div class="sub">Δ ≤ -0.2 GPA</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card info-card"><h3>Stable</h3><p>{((student_sem["delta"]>-0.2)&(student_sem["delta"]<0.2)).sum()}</p><div class="sub">|Δ| &lt; 0.2 GPA</div></div>', unsafe_allow_html=True)
    st.write("")

    trend_filter = st.selectbox("Filter by Trend", ["All","📈 Improved","📉 Declined","➖ Stable"], key="trend_filter")
    major_filter = st.selectbox("Filter by Department", ["All"] + sorted(data['major'].unique().tolist()), key="improve_major")
    view = student_sem.copy()
    if trend_filter != "All": view = view[view['Trend'] == trend_filter]
    if major_filter != "All": view = view[view['major'] == major_filter]
    view['Term'] = view['semester'] + ' ' + view['year'].astype(str)
    view['gpa']  = view['gpa'].round(2)

    display = view.rename(columns={'student_id':'ID','first_name':'First','last_name':'Last','major':'Major','gpa':'GPA','delta':'ΔGPA'})
    st.dataframe(display[['ID','First','Last','Major','Term','GPA','ΔGPA','Trend']].sort_values('ΔGPA'), use_container_width=True)
    st.download_button("⬇ Download Improvement Report (CSV)", view.to_csv(index=False), "improvement_tracking.csv", "text/csv")

    col1, col2 = st.columns(2)
    with col1:
        trend_count = student_sem['Trend'].value_counts().reset_index()
        trend_count.columns = ['Trend','Count']
        color_map = {'📈 Improved':'#10B981','📉 Declined':'#EF4444','➖ Stable':'#F59E0B'}
        fig = px.bar(trend_count, x='Trend', y='Count', color='Trend',
                     title='Students by Trend Category',
                     color_discrete_map=color_map)
        st.plotly_chart(transparent_layout(fig), use_container_width=True)
    with col2:
        fig = px.histogram(student_sem, x='delta', nbins=30, title='GPA Change Distribution',
                           color_discrete_sequence=['#60A5FA'])
        fig.add_vline(x=0, line_dash='dash', line_color='white', annotation_text='No Change')
        st.plotly_chart(transparent_layout(fig), use_container_width=True)


# ─── Page: PDF Transcript ──────────────────────────────────────────────────────
def render_pdf_transcript(data, system):
    st.markdown('<p class="section-title">🖨 Print-Ready PDF Transcript</p>', unsafe_allow_html=True)
    st.caption("Generate a professionally formatted PDF transcript for any student")

    sid = st.text_input("Enter Student ID or Name", key="pdf_search", placeholder="e.g. 1042 or James Smith")
    if st.button("Generate PDF", key="gen_pdf") and sid:
        student_details, course_history = system.get_student_details(sid)
        if student_details is not None and not student_details.empty:
            for _, student in student_details.iterrows():
                sc = course_history[course_history['student_id'] == student['student_id']].sort_values(['year','semester']).copy()
                sc['Letter'] = sc['grade'].apply(letter_grade)

                try:
                    from fpdf import FPDF
                    import io

                    class TranscriptPDF(FPDF):
                        def header(self):
                            self.set_fill_color(15, 23, 42)
                            self.rect(0, 0, 210, 40, 'F')
                            self.set_font('Helvetica', 'B', 20)
                            self.set_text_color(255, 255, 255)
                            self.set_y(10)
                            self.cell(0, 10, 'ACADEMIX', align='C', ln=True)
                            self.set_font('Helvetica', '', 10)
                            self.set_text_color(148, 163, 184)
                            self.cell(0, 6, 'Official Academic Transcript', align='C', ln=True)
                            self.ln(5)

                        def footer(self):
                            self.set_y(-15)
                            self.set_font('Helvetica', 'I', 8)
                            self.set_text_color(100, 116, 139)
                            self.cell(0, 10, f'Page {self.page_no()} | Generated by AcademiX School Analytics Platform', align='C')

                    pdf = TranscriptPDF()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.add_page()
                    pdf.set_margins(15, 45, 15)

                    # Student info block
                    pdf.set_fill_color(30, 41, 59)
                    pdf.set_draw_color(59, 130, 246)
                    pdf.set_line_width(0.5)
                    pdf.rect(15, 45, 180, 38, 'FD')
                    pdf.set_text_color(96, 165, 250)
                    pdf.set_font('Helvetica', 'B', 13)
                    pdf.set_y(49)
                    pdf.cell(0, 7, f"{student['first_name']} {student['last_name']}", align='C', ln=True)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.set_text_color(148, 163, 184)
                    pdf.cell(0, 5, f"Student ID: {student['student_id']}   |   Major: {student['major']}   |   CGPA: {student['cgpa']:.2f}/4.0 ({letter_grade(student['cgpa'])})", align='C', ln=True)
                    pdf.cell(0, 5, f"Email: {student.get('email','N/A')}   |   Total Credits: {student['credits']}", align='C', ln=True)
                    pdf.ln(12)

                    # Table header
                    pdf.set_fill_color(59, 130, 246)
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font('Helvetica', 'B', 9)
                    cols = [('Course', 28), ('Name', 48), ('Semester', 28), ('Year', 18), ('Grade', 18), ('Letter', 17), ('Credits', 23)]
                    for h, w in cols:
                        pdf.cell(w, 8, h, border=0, fill=True, align='C')
                    pdf.ln()

                    # Table rows
                    pdf.set_font('Helvetica', '', 8)
                    for i, (_, row) in enumerate(sc.iterrows()):
                        fill = i % 2 == 0
                        pdf.set_fill_color(30, 41, 59) if fill else pdf.set_fill_color(15, 23, 42)
                        pdf.set_text_color(226, 232, 240)
                        vals = [str(row['course_code']), str(row['course_name'])[:22],
                                str(row['semester']), str(row['year']),
                                f"{row['grade']:.2f}", str(row['Letter']), str(row['credits'])]
                        for (_, w), v in zip(cols, vals):
                            pdf.cell(w, 7, v, fill=True, align='C')
                        pdf.ln()

                    # Summary footer box
                    pdf.ln(5)
                    pdf.set_fill_color(15, 23, 42)
                    pdf.set_draw_color(16, 185, 129)
                    pdf.set_line_width(0.4)
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.set_text_color(52, 211, 153)
                    pdf.cell(0, 8, f"Cumulative GPA: {student['cgpa']:.2f}/4.0 ({letter_grade(student['cgpa'])})    Total Credits: {student['credits']}", align='C', ln=True)

                    # Output
                    pdf_bytes = bytes(pdf.output())
                    st.success(f"✅ PDF ready for {student['first_name']} {student['last_name']}!")
                    col1, col2 = st.columns(2)
                    col1.download_button(
                        label="⬇ Download PDF Transcript",
                        data=pdf_bytes,
                        file_name=f"transcript_{student['student_id']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    col2.info("📌 Open the PDF in any browser or Acrobat to print.")

                except ImportError:
                    st.error("fpdf2 not installed. Run: pip install fpdf2")
        else:
            st.error("Student not found.")

def main():
    # ── Show login success toast ──
    if st.session_state.get('just_logged_in', False):
        st.toast('✅ Logged in successfully!', icon='🎉')
        st.session_state.just_logged_in = False

    # ── Check for logout via query param ──
    if st.query_params.get('logout') == '1':
        st.session_state.authenticated = False
        st.session_state.logged_in_user = None
        st.session_state.just_logged_in = False
        st.query_params.clear()
        st.rerun()

    # ── Top-right user profile + logout icon (pure HTML/CSS, always positioned correctly) ──
    logged_user = st.session_state.get('logged_in_user', 'User')
    st.markdown(f"""
    <style>
        .user-topbar {{
            position: fixed; top: 15px; right: 20px; z-index: 1000000;
            display: flex; align-items: center;
            font-family: 'Inter', sans-serif;
        }}
        .user-pill-top {{
            display: flex; align-items: center; gap: 0;
            background: rgba(15,23,42,0.6);
            border: 1px solid rgba(124,58,237,.25);
            border-radius: 25px; padding: 4px 4px 4px 5px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .user-av-top {{
            width: 28px; height: 28px; border-radius: 50%;
            background: linear-gradient(135deg, #7C3AED, #3B82F6);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; color: white; font-weight: 700;
            flex-shrink: 0;
        }}
        .user-nm-top {{
            color: #E2E8F0; font-size: .8rem; font-weight: 600;
            letter-spacing: .3px; padding: 0 10px 0 8px;
        }}
        .pill-divider {{
            width: 1px; height: 20px; background: rgba(255,255,255,.12);
        }}
        .logout-icon-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 30px; height: 30px; border-radius: 50%;
            background: transparent;
            border: none;
            color: #94A3B8; font-size: 1rem;
            cursor: pointer; text-decoration: none;
            transition: all .2s ease;
            margin-left: 2px;
        }}
        .logout-icon-btn:hover {{
            background: rgba(239,68,68,.15);
            color: #FCA5A5;
        }}
    </style>
    <div class="user-topbar">
        <div class="user-pill-top">
            <div class="user-av-top">{logged_user[0].upper()}</div>
            <span class="user-nm-top">{logged_user}</span>
            <div class="pill-divider"></div>
            <a href="?logout=1" class="logout-icon-btn" title="Logout" target="_self">⏻</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ──
    with st.sidebar:
        # ── Branding ──
        st.markdown("""
        <div style="text-align:center; padding:1.2rem 0 0.8rem;">
            <div style="font-size:2.5rem; filter:drop-shadow(0 0 12px rgba(96,165,250,.4))">🎓</div>
            <div style="font-weight:800; font-size:1.1rem; color:#E2E8F0; letter-spacing:.5px; margin-top:.3rem;">AcademiX</div>
            <div style="font-size:.65rem; color:#475569; margin-top:.15rem; letter-spacing:1px; text-transform:uppercase;">Student Analytics Platform</div>
        </div>
        """, unsafe_allow_html=True)

        def nav_section(label):
            st.markdown(f"""
            <div style="padding:.35rem .5rem .15rem; margin-top:.4rem;">
                <span style="font-size:.65rem; font-weight:700; letter-spacing:1.5px;
                             text-transform:uppercase; color:#334155;">
                    {label}
                </span>
            </div>""", unsafe_allow_html=True)

        # ── Single navigation radio (only ONE dot ever shown) ────────────────
        all_pages = [
            "🏠 Welcome", "📊 Dashboard",
            "── ACADEMIC MONITORING ──",
            "🚨 At-Risk Students", "🏆 Top Performers", "🔔 Improvement",
            "── REPORTS & ANALYSIS ──",
            "🏫 Dept Overview", "📋 Attendance", "🎯 Pass/Fail", "📊 Batch Compare",
            "── STUDENT RECORDS ──",
            "🔍 Student Search", "📅 Semester Report", "📄 Transcript", "🖨 PDF Transcript",
            "── DATA ──",
            "📈 Statistics", "📂 Upload Data",
        ]
        # Dynamic CSS logic:
        # We explicitly control EACH label by its index for absolute reliability.
        dynamic_css = ""
        for idx, item in enumerate(all_pages):
            css_idx = idx + 1 # nth-of-type is 1-indexed
            
            if item.startswith("──"):
                # Header Styling: No dot, centered dimmed caps, non-clickable
                dynamic_css += f"""
                section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:nth-of-type({css_idx}) {{
                    pointer-events: none !important; padding-top: 1.5rem !important; margin-bottom: 0.2rem !important; opacity: 1 !important;
                }}
                section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:nth-of-type({css_idx})::before {{
                    display: none !important;
                }}
                section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:nth-of-type({css_idx}) p {{
                    color: #475569 !important; font-size: 0.68rem !important; font-weight: 800 !important; 
                    letter-spacing: 1.2px !important; text-transform: uppercase !important; text-align: center !important; 
                    width: 100% !important; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 4px;
                }}
                """
            else:
                # Functional Page Styling: Show the custom point
                dynamic_css += f"""
                section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:nth-of-type({css_idx})::before {{
                    display: inline-block !important;
                }}
                """
        
        st.markdown(f"<style>{dynamic_css}</style>", unsafe_allow_html=True)




        # Use index of active_page to keep sidebar in sync
        cur_page = st.session_state.get('active_page', '🏠 Welcome')
        cur_idx = all_pages.index(cur_page) if cur_page in all_pages else 0

        selected = st.radio(
            "Navigation", all_pages,
            index=cur_idx,
            label_visibility="collapsed",
            key="main_nav"
        )
        # If user picked a section header, ignore it and keep previous page
        if selected and not selected.startswith("──"):
            if st.session_state.get('active_page') != selected:
                st.session_state.active_page = selected
                st.rerun()


        choice = st.session_state.active_page

        # ── User Profile + Logout at bottom of sidebar ──
        st.markdown("""<hr style="border:none; border-top:1px solid rgba(96,165,250,.12); margin:1.2rem 0 .8rem;">""", unsafe_allow_html=True)
        logged_user = st.session_state.get('logged_in_user', 'User')
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding:0.5rem 0.6rem;
                    background:linear-gradient(135deg, rgba(124,58,237,.08), rgba(96,165,250,.08));
                    border:1px solid rgba(124,58,237,.18); border-radius:12px; margin-bottom:0.6rem;">
            <div style="width:32px; height:32px; border-radius:50%;
                        background:linear-gradient(135deg, #7C3AED, #3B82F6);
                        display:flex; align-items:center; justify-content:center;
                        font-size:14px; color:white; font-weight:700; flex-shrink:0;">{logged_user[0].upper()}</div>
            <div>
                <div style="font-size:.82rem; font-weight:600; color:#E2E8F0;">{logged_user}</div>
                <div style="font-size:.65rem; color:#64748B;">Signed in</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button('🚪 Logout', key='sidebar_logout_btn', use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.logged_in_user = None
            st.session_state.just_logged_in = False
            st.rerun()

    # ── Init system ──
    if st.session_state.system is None:
        st.session_state.system = StudentRecordsSystem()
    system = st.session_state.system
    data   = system.data

    no_data_pages = ["📊 Dashboard","🚨 At-Risk Students","🏆 Top Performers",
                     "📋 Attendance","🏫 Dept Overview","� Semester Report",
                     "📊 Batch Compare","🎯 Pass/Fail","🔔 Improvement",
                     "�🔍 Student Search","📄 Transcript","🖨 PDF Transcript","📈 Statistics"]

    # ── Routing ──
    if choice == "🏠 Welcome":
        render_landing(system)

    elif data is None and choice in no_data_pages:
        # ── Premium Empty State with 3D Background ──
        st.markdown("""
        <style>
            /* ── Main Content 3D Background ── */
            .main-3d-bg { position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
            .main-3d-bg .bg-orb1 { position:absolute; top:15%; right:10%; width:300px; height:300px; border-radius:50%; background:radial-gradient(circle, rgba(167,139,250,.06), transparent 70%); filter:blur(40px); animation:mainOrbFloat 20s ease-in-out infinite alternate; }
            .main-3d-bg .bg-orb2 { position:absolute; bottom:10%; left:5%; width:400px; height:400px; border-radius:50%; background:radial-gradient(circle, rgba(59,130,246,.05), transparent 70%); filter:blur(50px); animation:mainOrbFloat 25s ease-in-out infinite alternate-reverse; }
            .main-3d-bg .bg-orb3 { position:absolute; top:50%; left:50%; width:250px; height:250px; border-radius:50%; background:radial-gradient(circle, rgba(52,211,153,.04), transparent 70%); filter:blur(35px); animation:mainOrbFloat 18s ease-in-out infinite alternate; }
            @keyframes mainOrbFloat { 0%{transform:translateY(0) scale(1);} 100%{transform:translateY(-30px) scale(1.1);} }
            
            .main-3d-bg .bg-orbital { position:absolute; top:20%; right:15%; width:90px; height:90px; transform-style:preserve-3d; animation:mainOrbitalRot 30s linear infinite; opacity:0.6; }
            .main-3d-bg .bg-orbital .ring { position:absolute; width:100%; height:100%; border:2px solid rgba(167,139,250,.3); border-radius:50%; }
            .main-3d-bg .bg-orbital .r1 { transform: rotateX(65deg) rotateY(0deg); border-color: rgba(96,165,250,.3); }
            .main-3d-bg .bg-orbital .r2 { transform: rotateX(65deg) rotateY(60deg); border-color: rgba(167,139,250,.3); }
            .main-3d-bg .bg-orbital .r3 { transform: rotateX(65deg) rotateY(120deg); border-color: rgba(52,211,153,.3); }
            .main-3d-bg .bg-orbital .core { position:absolute; top:50%; left:50%; width:16px; height:16px; background:radial-gradient(circle, #8B5CF6, transparent); border-radius:50%; transform:translate(-50%,-50%); box-shadow:0 0 20px rgba(139,92,246,.5); }
            @keyframes mainOrbitalRot { 0%{transform:rotateX(0) rotateY(0) rotateZ(0);} 100%{transform:rotateX(360deg) rotateY(360deg) rotateZ(360deg);} }
            
            .main-3d-bg .bg-orbital2 { position:absolute; bottom:25%; left:12%; width:60px; height:60px; transform-style:preserve-3d; animation:mainOrbitalRot 22s linear infinite reverse; opacity:0.5; }
            .main-3d-bg .bg-orbital2 .ring { position:absolute; width:100%; height:100%; border:1.5px solid rgba(34,211,238,.3); border-radius:50%; }
            .main-3d-bg .bg-orbital2 .r1 { transform: rotateX(65deg) rotateY(0deg); }
            .main-3d-bg .bg-orbital2 .r2 { transform: rotateX(65deg) rotateY(60deg); border-color: rgba(59,130,246,.3); }
            .main-3d-bg .bg-orbital2 .r3 { transform: rotateX(65deg) rotateY(120deg); }
            .main-3d-bg .bg-orbital2 .core { position:absolute; top:50%; left:50%; width:10px; height:10px; background:radial-gradient(circle, #38BDF8, transparent); border-radius:50%; transform:translate(-50%,-50%); box-shadow:0 0 15px rgba(56,189,248,.5); }

            /* ── Premium Empty State Card Container ── */
            [data-testid="stVerticalBlockBorderWrapper"]:has(#empty-card-anchor) {
                width: 100% !important; max-width: 620px !important; margin: 3rem auto !important; padding: 3rem 2.5rem 1rem !important;
                background: rgba(15, 23, 42, 0.6) !important;
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(167,139,250,.15) !important;
                border-radius: 24px !important;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,.3), 0 0 40px rgba(167,139,250,.05) !important;
                position: relative; z-index: 2;
                animation: emptyCardPop .6s cubic-bezier(.34,1.56,.64,1) both;
            }
            @keyframes emptyCardPop { from{opacity:0; transform:scale(.9) translateY(20px);} to{opacity:1; transform:scale(1) translateY(0);} }
            
            .empty-icon {
                font-size: 4rem; margin-bottom: 1rem; text-align: center; display: block;
                animation: emptyIconFloat 4s ease-in-out infinite;
                filter: drop-shadow(0 8px 20px rgba(167,139,250,.3));
            }
            @keyframes emptyIconFloat { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-12px);} }
            
            .empty-title {
                font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px;
                background: linear-gradient(135deg, #E2E8F0 0%, #A78BFA 50%, #60A5FA 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
                margin-bottom: 0.5rem; text-align: center; display: block;
            }
            .empty-desc {
                font-size: 0.95rem; color: #94A3B8; line-height: 1.6;
                max-width: 450px; margin: 0 auto 1.5rem; text-align: center; display: block;
            }
            
            /* Style the Streamlit button inside our card */
            [data-testid="stVerticalBlockBorderWrapper"]:has(#empty-card-anchor) [data-testid="baseButton-secondary"] {
                background: linear-gradient(135deg, #7C3AED, #3B82F6) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0.8rem 2rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                box-shadow: 0 4px 15px rgba(124,58,237,.4) !important;
                transition: all .2s ease !important;
                margin: 0.5rem auto 1.5rem !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"]:has(#empty-card-anchor) [data-testid="baseButton-secondary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(124,58,237,.6) !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"]:has(#empty-card-anchor) [data-testid="baseButton-secondary"] p {
                color: white !important; font-weight: 600 !important; font-size: 1rem !important;
            }
            
            .empty-features { display:flex; gap:1.5rem; justify-content:center; margin-top:2rem; flex-wrap:wrap; }
            .empty-feature {
                display:flex; align-items:center; gap:8px;
                font-size:.8rem; color:#64748B;
            }
            .empty-feature-dot { width:6px; height:6px; border-radius:50%; background:linear-gradient(135deg,#7C3AED,#3B82F6); flex-shrink:0; }
        </style>
        
        <div class="main-3d-bg">
            <div class="bg-orb1"></div>
            <div class="bg-orb2"></div>
            <div class="bg-orb3"></div>
            <div class="bg-orbital"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
            <div class="bg-orbital2"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # We use a Streamlit container so the button acts naturally inside it
        with st.container(border=True):
            st.markdown('<div id="empty-card-anchor"></div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="empty-icon">📊</div>
                <div class="empty-title">No Data Loaded Yet</div>
                <div class="empty-desc">
                    Load your student records to unlock powerful analytics — track grades, attendance, at-risk students, and generate professional transcripts.
                </div>
            """, unsafe_allow_html=True)
            
            _, col_btn, _ = st.columns([1.5, 2, 1.5])
            with col_btn:
                def go_to_welcome():
                    st.session_state.active_page = "🏠 Welcome"
                    st.session_state.main_nav = "🏠 Welcome"
                    
                st.button("🏠  Go to Welcome", key="empty_go_welcome", on_click=go_to_welcome, use_container_width=True)

            st.markdown("""
                <div class="empty-features">
                    <div class="empty-feature"><div class="empty-feature-dot"></div>15+ Analytics Views</div>
                    <div class="empty-feature"><div class="empty-feature-dot"></div>PDF Transcripts</div>
                    <div class="empty-feature"><div class="empty-feature-dot"></div>At-Risk Detection</div>
                    <div class="empty-feature"><div class="empty-feature-dot"></div>Batch Comparisons</div>
                </div>
            """, unsafe_allow_html=True)

    elif choice == "📊 Dashboard":
        # ── Enhanced Dashboard Header ──
        st.markdown("""
        <style>
            .dash-header { text-align:center; margin-bottom:2rem; position:relative; z-index:2; }
            .dash-title {
                font-size:2.2rem; font-weight:800; letter-spacing:-1px;
                background:linear-gradient(135deg, #A78BFA 0%, #60A5FA 50%, #34D399 100%);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
                margin-bottom:0.3rem;
            }
            .dash-sub { font-size:0.95rem; color:#64748B; font-weight:400; }
            .dash-divider { width:80px; height:3px; background:linear-gradient(90deg,#7C3AED,#3B82F6,#22D3EE); border-radius:2px; margin:0.8rem auto 0; }
        </style>
        <div class="dash-header">
            <div class="dash-title">📊 Overview Dashboard</div>
            <div class="dash-sub">Real-time academic performance insights across your institution</div>
            <div class="dash-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        if data is None or data.empty or 'student_id' not in data.columns:
            st.warning("⚠️ No data available to display. Please go to the Welcome page and load your student records first.")
            return

        student_agg = data.groupby('student_id').agg(cgpa=('grade','mean'), attendance=('attendance','mean')).reset_index()
        at_risk_n  = ((student_agg['cgpa'] < 2.0) | (student_agg['attendance'] < 0.75)).sum()
        top_perf_n = (student_agg['cgpa'] >= 3.5).sum()
        total_stu  = student_agg['student_id'].nunique()
        avg_gpa    = student_agg['cgpa'].mean()
        avg_att    = student_agg['attendance'].mean()

        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card info-card"><h3>Total Students</h3><p>{total_stu}</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card success-card"><h3>Avg GPA</h3><p>{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card warning-card"><h3>Avg Attendance</h3><p>{avg_att*100:.1f}%</p></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card danger-card"><h3>At-Risk</h3><p>{at_risk_n}</p></div>', unsafe_allow_html=True)
        st.write("")

        r2c1, r2c2 = st.columns(2)
        r2c1.markdown(f'<div class="metric-card success-card"><h3>🏆 Top Performers</h3><p>{top_perf_n}</p><div class="sub">GPA ≥ 3.5</div></div>', unsafe_allow_html=True)
        r2c2.markdown(f'<div class="metric-card info-card"><h3>📚 Total Credits Earned</h3><p>{int(data["credits"].sum()):,}</p></div>', unsafe_allow_html=True)
        st.write("")

        ch1, ch2 = st.columns(2)
        with ch1:
            major_gpa = data.groupby('major')['grade'].mean().reset_index().sort_values('grade', ascending=False)
            fig = px.bar(major_gpa, x='grade', y='major', orientation='h',
                         title='Avg GPA by Department', color='grade',
                         color_continuous_scale='Blues', range_color=[2,4])
            st.plotly_chart(transparent_layout(fig), use_container_width=True)
        with ch2:
            fig = px.histogram(data, x='grade', nbins=20, title='Grade Distribution',
                               color_discrete_sequence=['#A78BFA'])
            st.plotly_chart(transparent_layout(fig), use_container_width=True)

        sem = data.groupby(['year','semester']).agg(avg_gpa=('grade','mean')).reset_index()
        sem['term'] = sem['semester'] + ' ' + sem['year'].astype(str)
        sem = sem.sort_values(['year','semester'])
        fig = px.line(sem, x='term', y='avg_gpa', markers=True,
                      title='Semester-wise Average GPA Trend', color_discrete_sequence=['#60A5FA'])
        st.plotly_chart(transparent_layout(fig), use_container_width=True)

    elif choice == "🚨 At-Risk Students":
        render_at_risk(data)

    elif choice == "🏆 Top Performers":
        render_top_performers(data)

    elif choice == "📋 Attendance":
        render_attendance(data)

    elif choice == "🔍 Student Search":
        st.markdown('<p class="section-title">🔍 Student Search</p>', unsafe_allow_html=True)
        search_input = st.text_input("Enter Student ID or Name", placeholder="e.g. 1042 or James Smith")
        if st.button("Search") and search_input:
            student_details, course_history = system.get_student_details(search_input)
            if student_details is not None and not student_details.empty:
                for _, student in student_details.iterrows():
                    att_pct  = student['overall_attendance']*100
                    gpa_pill = '<span class="pill pill-green">✓ Good</span>' if student['cgpa'] >= 2.0 else '<span class="pill pill-red">⚠ Low GPA</span>'
                    att_pill = '<span class="pill pill-green">✓ Good</span>' if att_pct >= 75 else '<span class="pill pill-red">⚠ Low Att.</span>'
                    st.markdown(f"""
                    <div class="student-info">
                        <h3>👤 {student['first_name']} {student['last_name']}</h3>
                        <strong>Student ID:</strong> {student['student_id']}&nbsp;
                        <strong>Major:</strong> {student['major']}<br>
                        <strong>Email:</strong> {student.get('email','N/A')}&nbsp;
                        <strong>Phone:</strong> {student.get('phone','N/A')}<br>
                        <strong>CGPA:</strong> {student['cgpa']:.2f} {gpa_pill}&nbsp;
                        <strong>Attendance:</strong> {att_pct:.1f}% {att_pill}
                    </div>""", unsafe_allow_html=True)
                    col1,col2,col3 = st.columns(3)
                    col1.metric("CGPA", f"{student['cgpa']:.2f}/4.0")
                    col2.metric("Attendance", f"{att_pct:.1f}%")
                    col3.metric("Credits", student['credits'])
                    st.markdown("---")
                    st.subheader("📚 Course History")
                    sc = course_history[course_history['student_id'] == student['student_id']]
                    st.dataframe(sc[['course_code','course_name','semester','year','grade','attendance','credits']], use_container_width=True)
                    t1,t2,t3,t4 = st.tabs(["📊 Basic","📈 Trends","🔗 Correlations","📉 Progression"])
                    with t1:
                        cc1,cc2 = st.columns(2)
                        cc1.plotly_chart(transparent_layout(plot_grades_by_course(sc)), use_container_width=True)
                        cc2.plotly_chart(transparent_layout(plot_attendance_by_course(sc)), use_container_width=True)
                        cc1,cc2 = st.columns(2)
                        cc1.plotly_chart(transparent_layout(plot_grade_distribution(sc)), use_container_width=True)
                        cc2.plotly_chart(transparent_layout(plot_credit_distribution(sc)), use_container_width=True)
                    with t2:
                        st.plotly_chart(transparent_layout(plot_semester_trend(sc)), use_container_width=True)
                    with t3:
                        st.plotly_chart(transparent_layout(plot_grade_vs_attendance(sc)), use_container_width=True)
                        st.plotly_chart(transparent_layout(plot_performance_by_level(sc)), use_container_width=True)
                    with t4:
                        st.plotly_chart(plot_progression(sc), use_container_width=True)
            else:
                st.error("No student found with that identifier.")

    elif choice == "📄 Transcript":
        st.markdown('<p class="section-title">📄 Generate Transcript</p>', unsafe_allow_html=True)
        sid = st.text_input("Enter Student ID or Name", key="transcript_search")
        if st.button("Generate") and sid:
            student_details, course_history = system.get_student_details(sid)
            if student_details is not None and not student_details.empty:
                for _, student in student_details.iterrows():
                    sc = course_history[course_history['student_id'] == student['student_id']].sort_values(['year','semester'])
                    sc = sc.copy()
                    sc['Letter'] = sc['grade'].apply(letter_grade)
                    sc['Att%']   = (sc['attendance']*100).round(1).astype(str) + '%'
                    st.markdown(f"""
                    <div class="student-info">
                        <h3>🎓 Official Academic Transcript</h3>
                        <strong>Name:</strong> {student['first_name']} {student['last_name']}&nbsp;
                        <strong>ID:</strong> {student['student_id']}<br>
                        <strong>Major:</strong> {student['major']}&nbsp;
                        <strong>CGPA:</strong> {student['cgpa']:.2f}/4.0 ({letter_grade(student['cgpa'])})&nbsp;
                        <strong>Credits:</strong> {student['credits']}
                    </div>""", unsafe_allow_html=True)
                    st.dataframe(sc[['course_code','course_name','semester','year','grade','Letter','Att%','credits']], use_container_width=True)
                    txt = f"OFFICIAL TRANSCRIPT\n{'='*50}\n"
                    txt += f"Name: {student['first_name']} {student['last_name']}\n"
                    txt += f"ID: {student['student_id']}  Major: {student['major']}\n"
                    txt += f"CGPA: {student['cgpa']:.2f}/4.0  Credits: {student['credits']}\n\nCOURSE HISTORY:\n{'-'*50}\n"
                    for _, r in sc.iterrows():
                        txt += f"{r['course_code']} | {r['semester']} {r['year']} | Grade: {r['grade']} ({r['Letter']}) | Att: {r['Att%']} | {r['credits']} cr\n"
                    txt += "\n--- END OF TRANSCRIPT ---"
                    cc1,cc2 = st.columns(2)
                    cc1.download_button("⬇ Download TXT", txt, f"transcript_{student['student_id']}.txt", "text/plain")
                    cc2.download_button("⬇ Download CSV", sc.to_csv(index=False), f"courses_{student['student_id']}.csv", "text/csv")
            else:
                st.error("Student not found.")


    elif choice == "🏫 Dept Overview":
        render_department_overview(data)

    elif choice == "📅 Semester Report":
        render_semester_report(data, system)

    elif choice == "📊 Batch Compare":
        render_batch_comparison(data)

    elif choice == "🎯 Pass/Fail":
        render_pass_fail(data)

    elif choice == "🔔 Improvement":
        render_improvement_tracking(data)

    elif choice == "🖨 PDF Transcript":
        render_pdf_transcript(data, system)

    elif choice == "📈 Statistics":
        st.markdown('<p class="section-title">📈 Dataset Statistics</p>', unsafe_allow_html=True)
        stats = system.dataset_statistics()
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Records",   stats['total_records'])
        c2.metric("Unique Students", stats['unique_students'])
        c3.metric("Unique Courses",  stats['unique_courses'])
        c1.metric("Year Range",  f"{stats['min_year']} – {stats['max_year']}")
        c2.metric("Avg GPA",     f"{stats['avg_gpa']:.2f}")
        c3.metric("Avg Attendance", f"{stats['avg_attendance']*100:.1f}%")
        top_df = pd.DataFrame(list(stats['top_majors'].items()), columns=['Major','Count'])
        fig = px.bar(top_df, x='Count', y='Major', orientation='h', title='Top Majors',
                     color='Count', color_continuous_scale='Blues')
        st.plotly_chart(transparent_layout(fig), use_container_width=True)
        fig = px.box(data, x='major', y='grade', title='GPA Distribution by Major')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(transparent_layout(fig), use_container_width=True)
        fig = px.scatter(data, x='attendance', y='grade', color='major', opacity=0.5,
                         title='Attendance vs Grade', labels={'attendance':'Attendance','grade':'Grade'})
        fig.update_xaxes(tickformat='.0%')
        st.plotly_chart(transparent_layout(fig), use_container_width=True)

    elif choice == "📂 Upload Data":
        st.markdown('<p class="section-title">📂 Upload Dataset</p>', unsafe_allow_html=True)
        st.info("Upload a CSV file with student records. Required columns include: student_id, first_name, last_name, major, course_code, grade, attendance, credits, semester, year.")
        if st.button("🗂 Load Demo Data Instead"):
            with st.spinner("Generating…"):
                system.load_data()
                st.session_state.data = system.data
            st.success("Demo data loaded!")
        st.markdown("---")
        uploaded = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded:
            with st.spinner("Loading…"):
                ok = system.load_data(uploaded)
                if ok:
                    st.session_state.data = system.data
                    st.success("Data loaded successfully!")
                    st.dataframe(system.data.head(10))
                else:
                    st.error("Failed to load. Check file format.")

    # ── Footer ──
    st.markdown("""
        <div class="footer-container">
            <p style="font-weight:600;color:#E5E7EB;margin-bottom:.3rem;">🎓 AcademiX — School Analytics Platform</p>
            <p style="margin-bottom:1rem;color:#94A3B8;">Built with <a href="https://streamlit.io" target="_blank">Streamlit</a> and <a href="https://plotly.com" target="_blank">Plotly</a> 🚀</p>
            <div style="display:flex;gap:20px;justify-content:center;align-items:center;margin-bottom:1rem;">
                <a href="https://github.com/sathishr-ai/student-academic-analytics-platform" target="_blank"
                   style="opacity:0.8;transition:opacity 0.2s;" title="GitHub">
                    <img src="https://img.icons8.com/ios/32/FFFFFF/github.png" width="26" height="26"
                         style="border-radius:50%;display:block;">
                </a>
                <a href="https://www.linkedin.com/in/sathish-r-2393412a5" target="_blank"
                   style="opacity:0.8;transition:opacity 0.2s;" title="LinkedIn">
                    <img src="https://img.icons8.com/ios/32/0A66C2/linkedin.png" width="26" height="26"
                         style="border-radius:4px;display:block;">
                </a>
            </div>
            <p style="font-size:.72rem;color:#475569;">© 2026 Sathish R. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)


# ─── Authentication Gate ───────────────────────────────────────────────────────
def render_login_page():
    """Render a Streamlit-native login page styled to match the custom login.html design."""

    # Hide sidebar and Streamlit chrome, inject ALL login CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        [data-testid="stSidebar"]     { display: none !important; }
        [data-testid="stHeader"]      { display: none !important; }
        [data-testid="stToolbar"]     { display: none !important; }
        footer, #MainMenu             { display: none !important; }
        .stApp                        { background: #070b16 !important; }
        .stMainBlockContainer,
        [data-testid="stAppViewBlockContainer"],
        .block-container { padding: 0 !important; max-width: 100% !important; }
        .stTextInput > div > div > input {
            background: rgba(255,255,255,.04) !important;
            border: 1px solid rgba(255,255,255,.09) !important;
            border-radius: 10px !important; color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.88rem !important; font-weight: 500 !important;
            padding: 0.72rem 0.9rem !important; caret-color: #A78BFA !important;
        }
        .stTextInput > div > div > input:focus {
            background: rgba(167,139,250,.07) !important;
            border-color: rgba(167,139,250,.5) !important;
            box-shadow: 0 0 0 3px rgba(167,139,250,.1), 0 0 14px rgba(167,139,250,.14) !important;
        }
        .stTextInput > div > div > input::placeholder { color: #64748B !important; font-weight: 400 !important; }
        .stTextInput label {
            font-size: .72rem !important; font-weight: 700 !important;
            color: #94A3B8 !important; letter-spacing: .6px !important;
            text-transform: uppercase !important;
        }
        div.stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #7C3AED, #3B82F6 55%, #2563EB) !important;
            color: white !important; border: none !important; border-radius: 10px !important;
            padding: 0.85rem !important; font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important; font-weight: 700 !important;
            box-shadow: 0 4px 18px rgba(124,58,237,.4), 0 2px 7px rgba(59,130,246,.25) !important;
            transition: transform 0.2s, box-shadow 0.2s !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(124,58,237,.5), 0 3px 12px rgba(59,130,246,.35) !important;
        }
        .login-error {
            background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.28);
            color:#FCA5A5;border-radius:9px;padding:.65rem .9rem;font-size:.8rem;
            font-weight:500;margin-bottom:.8rem;display:flex;align-items:center;gap:7px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Two-column layout ──
    left_col, right_col = st.columns([55, 45], gap="small", vertical_alignment="center")

    # ── LEFT COLUMN: branding ──
    with left_col:
        st.html("""
        <style>
            .lp{position:relative;min-height:92vh;overflow:visible;
                background:linear-gradient(145deg,#060c1a,#0a1020 50%,#070e1d);
                padding:3.5rem 3rem;display:flex;flex-direction:column;justify-content:center;
                font-family:'Inter',sans-serif;}
            .lp::after{content:'';position:absolute;top:0;right:-1px;bottom:0;width:80px;
                background:linear-gradient(to bottom right,transparent 50%,#070b16 50%);pointer-events:none;}
            .lp-g{position:absolute;inset:0;pointer-events:none;
                background-image:linear-gradient(rgba(167,139,250,.04) 1px,transparent 1px),
                linear-gradient(90deg,rgba(167,139,250,.04) 1px,transparent 1px);background-size:52px 52px;}
            .lp-bl{position:absolute;border-radius:50%;filter:blur(100px);pointer-events:none;animation:lpD 9s ease-in-out infinite;}
            .b1{width:480px;height:480px;background:#A78BFA;top:-18%;left:-12%;opacity:.13;}
            .b2{width:360px;height:360px;background:#60A5FA;bottom:-14%;right:5%;opacity:.12;animation-direction:reverse;animation-duration:11s;}
            .b3{width:200px;height:200px;background:#22d3ee;top:55%;left:35%;opacity:.09;animation-delay:2s;animation-duration:7s;}
            @keyframes lpD{0%,100%{transform:translate(0,0) scale(1);}33%{transform:translate(25px,-20px) scale(1.05);}66%{transform:translate(-15px,18px) scale(.97);}}
            .lp-lo{display:flex;align-items:center;gap:10px;margin-bottom:2.8rem;animation:lpU .6s ease both;}
            .lp-li{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;
                background:linear-gradient(135deg,rgba(167,139,250,.25),rgba(96,165,250,.18));
                border:1px solid rgba(167,139,250,.35);font-size:1.4rem;box-shadow:0 0 20px rgba(167,139,250,.25);}
            .lp-ln{font-size:1.1rem;font-weight:800;letter-spacing:-.3px;
                background:linear-gradient(120deg,#E2E8F0,#A78BFA 60%,#60A5FA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
            .lp-t{font-size:2.7rem;font-weight:900;line-height:1.12;letter-spacing:-1.5px;margin-bottom:1rem;animation:lpU .6s ease .1s both;}
            .lp-t span{background:linear-gradient(120deg,#E2E8F0,#A78BFA 40%,#60A5FA 70%,#34D399);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
            .lp-s{font-size:1rem;color:#64748B;line-height:1.7;max-width:400px;margin-bottom:2.8rem;font-weight:400;animation:lpU .6s ease .2s both;}
            .lp-s strong{color:#94A3B8;font-weight:600;}
            .lp-fg{display:grid;grid-template-columns:1fr 1fr;gap:14px;animation:lpU .6s ease .3s both;}
            .lp-fc{background:linear-gradient(135deg,rgba(255,255,255,.045),rgba(255,255,255,.02));
                border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:1.15rem 1.05rem;
                position:relative;overflow:hidden;transition:transform .25s,border-color .25s,box-shadow .25s;}
            .lp-fc:hover{transform:translateY(-5px);border-color:rgba(167,139,250,.32);box-shadow:0 12px 32px rgba(0,0,0,.4);}
            .lp-fc::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
                background:linear-gradient(90deg,transparent,rgba(167,139,250,.35),transparent);}
            .fi{font-size:1.5rem;margin-bottom:.6rem;display:block;}
            .ft{font-size:.85rem;font-weight:700;color:#E2E8F0;margin-bottom:.28rem;}
            .fd{font-size:.74rem;color:#64748B;line-height:1.55;}
            @keyframes lpU{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}

            /* ── 3D Floating Geometric Shapes ────────────── */
            .scene-3d{position:absolute;inset:0;pointer-events:none;perspective:800px;overflow:hidden;z-index:1;}

            /* ── Shape 1: Orbital Data Rings ── */
            .shape-orbital{position:absolute;top:15%;right:8%;width:80px;height:80px;
                transform-style:preserve-3d;animation:orbitalFloat 12s ease-in-out infinite,orbitalRotate 18s linear infinite;}
            .shape-orbital .ring{position:absolute;width:100%;height:100%;border:2px solid rgba(167,139,250,.3);border-radius:50%;}
            .shape-orbital .r1 {transform:rotateX(65deg) rotateY(0deg); border-color: rgba(96,165,250,.4);}
            .shape-orbital .r2 {transform:rotateX(65deg) rotateY(60deg); border-color: rgba(167,139,250,.4);}
            .shape-orbital .r3 {transform:rotateX(65deg) rotateY(120deg); border-color: rgba(52,211,153,.4);}
            .shape-orbital .core{position:absolute;top:50%;left:50%;width:16px;height:16px;background:radial-gradient(circle, #60A5FA, transparent);border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 15px rgba(96,165,250,.6);}
            @keyframes orbitalRotate{0%{transform:rotateX(0) rotateY(0) rotateZ(0);}
                100%{transform:rotateX(360deg) rotateY(360deg) rotateZ(180deg);}}
            @keyframes orbitalFloat{0%,100%{top:15%;}50%{top:12%;}}

            /* ── Shape 2: Diamond / Octahedron ── */
            .shape-diamond{position:absolute;top:60%;left:12%;width:45px;height:45px;
                transform-style:preserve-3d;animation:diamondSpin 14s linear infinite,diamondFloat 10s ease-in-out infinite;}
            .shape-diamond::before,.shape-diamond::after{content:'';position:absolute;
                width:0;height:0;left:50%;transform:translateX(-50%);
                border-left:22px solid transparent;border-right:22px solid transparent;}
            .shape-diamond::before{top:-2px;border-bottom:32px solid rgba(96,165,250,.15);
                filter:drop-shadow(0 0 8px rgba(96,165,250,.3));}
            .shape-diamond::after{bottom:-2px;border-top:32px solid rgba(167,139,250,.15);
                filter:drop-shadow(0 0 8px rgba(167,139,250,.3));}
            @keyframes diamondSpin{0%{transform:rotateY(0) rotateZ(0);}100%{transform:rotateY(360deg) rotateZ(360deg);}}
            @keyframes diamondFloat{0%,100%{top:60%;}50%{top:56%;}}

            /* ── Shape 3: Secondary Orbitals ── */
            .shape-orbital-sm{position:absolute;top:35%;right:25%;width:50px;height:50px;
                transform-style:preserve-3d;animation:orbitalSmRot 20s linear infinite,orbitalSmFloat 8s ease-in-out infinite;}
            .shape-orbital-sm .ring{position:absolute;width:100%;height:100%;
                border:1.5px solid rgba(34,211,238,.3);border-radius:50%;}
            .shape-orbital-sm .r1 {transform:rotateX(65deg) rotateY(0deg);}
            .shape-orbital-sm .r2 {transform:rotateX(65deg) rotateY(60deg);border-color: rgba(59,130,246,.3);}
            .shape-orbital-sm .r3 {transform:rotateX(65deg) rotateY(120deg);}
            .shape-orbital-sm .core {position:absolute;top:50%;left:50%;width:10px;height:10px;background:radial-gradient(circle, #38BDF8, transparent);border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 15px rgba(56,189,248,.5);}
            @keyframes orbitalSmRot{0%{transform:rotateX(0) rotateY(0);}100%{transform:rotateX(-360deg) rotateY(360deg);}}
            @keyframes orbitalSmFloat{0%,100%{top:35%;}50%{top:32%;}}

            /* ── Shape 4: Orbital Ring ── */
            .shape-ring{position:absolute;top:22%;left:30%;width:80px;height:80px;
                border:1.5px solid rgba(167,139,250,.18);border-radius:50%;
                transform-style:preserve-3d;
                animation:ringOrbit 8s linear infinite;
                box-shadow:0 0 15px rgba(167,139,250,.1);}
            .shape-ring::after{content:'';position:absolute;top:-3px;left:50%;
                width:6px;height:6px;border-radius:50%;transform:translateX(-50%);
                background:#A78BFA;box-shadow:0 0 12px #A78BFA,0 0 25px rgba(167,139,250,.5);}
            @keyframes ringOrbit{0%{transform:rotateX(65deg) rotateZ(0);}100%{transform:rotateX(65deg) rotateZ(360deg);}}

            /* ── Shape 5: Floating Pyramid ── */
            .shape-pyramid{position:absolute;bottom:18%;right:18%;width:50px;height:50px;
                transform-style:preserve-3d;animation:pyrSpin 16s linear infinite,pyrFloat 9s ease-in-out infinite;}
            .pyr-face{position:absolute;width:0;height:0;
                border-left:25px solid transparent;border-right:25px solid transparent;
                border-bottom:45px solid rgba(167,139,250,.1);transform-origin:bottom center;}
            .pyr-f1{transform:rotateY(0deg) rotateX(30deg) translateZ(0);}
            .pyr-f2{transform:rotateY(90deg) rotateX(30deg) translateZ(0);}
            .pyr-f3{transform:rotateY(180deg) rotateX(30deg) translateZ(0);}
            .pyr-f4{transform:rotateY(270deg) rotateX(30deg) translateZ(0);}
            @keyframes pyrSpin{0%{transform:rotateY(0);}100%{transform:rotateY(360deg);}}
            @keyframes pyrFloat{0%,100%{bottom:18%;}50%{bottom:22%;}}

            /* ── Floating Glow Particles ── */
            .glow-particle{position:absolute;border-radius:50%;pointer-events:none;
                animation:particleFloat 6s ease-in-out infinite;}
            .gp1{width:4px;height:4px;background:#A78BFA;top:20%;left:45%;box-shadow:0 0 10px #A78BFA;animation-duration:5s;}
            .gp2{width:3px;height:3px;background:#60A5FA;top:70%;left:55%;box-shadow:0 0 8px #60A5FA;animation-delay:1.5s;animation-duration:7s;}
            .gp3{width:5px;height:5px;background:#22d3ee;top:45%;left:20%;box-shadow:0 0 12px #22d3ee;animation-delay:3s;animation-duration:6s;}
            .gp4{width:3px;height:3px;background:#A78BFA;top:80%;left:35%;box-shadow:0 0 8px #A78BFA;animation-delay:2s;animation-duration:8s;}
            .gp5{width:4px;height:4px;background:#60A5FA;top:10%;left:60%;box-shadow:0 0 10px #60A5FA;animation-delay:4s;animation-duration:5.5s;}
            @keyframes particleFloat{0%,100%{opacity:.6;transform:translateY(0) scale(1);}
                50%{opacity:1;transform:translateY(-20px) scale(1.3);}}
        </style>
        <div class="lp">
            <div class="lp-g"></div>
            <div class="lp-bl b1"></div><div class="lp-bl b2"></div><div class="lp-bl b3"></div>
            <!-- 3D Floating Geometric Shapes -->
            <div class="scene-3d">
                <div class="shape-orbital"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
                <div class="shape-orbital-sm"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
                <div class="shape-diamond"></div>
                <div class="shape-ring"></div>
                <div class="shape-pyramid"><div class="pyr-face pyr-f1"></div><div class="pyr-face pyr-f2"></div><div class="pyr-face pyr-f3"></div><div class="pyr-face pyr-f4"></div></div>
                <div class="glow-particle gp1"></div><div class="glow-particle gp2"></div><div class="glow-particle gp3"></div><div class="glow-particle gp4"></div><div class="glow-particle gp5"></div>
            </div>
            <div class="lp-lo"><div class="lp-li">🎓</div><span class="lp-ln">Student Analytics</span></div>
            <div class="lp-t"><span>Analyze. Understand.<br>Improve.</span></div>
            <p class="lp-s">A <strong>complete intelligence platform</strong> for institutions — track grades, attendance, at-risk students, top performers, and transcripts. All in one place.</p>
            <div class="lp-fg">
                <div class="lp-fc"><span class="fi">📊</span><div class="ft">Live Dashboard</div><div class="fd">Real-time KPIs — GPA, attendance &amp; at-risk counts.</div></div>
                <div class="lp-fc"><span class="fi">🚨</span><div class="ft">At-Risk Alerts</div><div class="fd">Flag students with low GPA or poor attendance.</div></div>
                <div class="lp-fc"><span class="fi">🏆</span><div class="ft">Top Performers</div><div class="fd">Honor roll leaderboard &amp; perfect attendance.</div></div>
                <div class="lp-fc"><span class="fi">📄</span><div class="ft">PDF Transcripts</div><div class="fd">Letter-graded, styled PDF or CSV export.</div></div>
            </div>
        </div>
        """)

    # ── RIGHT COLUMN: auth card ──
    with right_col:
        # Apply card styling via JS class injection
        st.markdown("""
        <style>
            /* ── Spinning Border Auth Card (High Compatibility) ── */
            [st-key="auth_card"] {
                max-width: 420px !important;
                margin: auto !important;
                position: relative !important;
            }
            [st-key="auth_card"] > [data-testid="stVerticalBlockBorderWrapper"],
            [st-key="auth_card"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: transparent !important; /* Let inner background handle it */
                border: none !important;
                padding: 0 !important;
                position: relative !important;
                z-index: 2 !important;
                box-shadow: 0 24px 64px rgba(0,0,0,.6) !important;
                animation: acPop .65s cubic-bezier(.34,1.56,.64,1) both, authCardFloat 8s ease-in-out infinite !important;
            }
            
            /* The Spinning Gradient Ring Layer */
            [st-key="auth_card"]::before {
                content: '';
                position: absolute;
                inset: -2px; /* 2px border thickness */
                border-radius: 24px;
                background: conic-gradient(
                    from 0deg,
                    rgba(11, 19, 38, 0.1) 0deg,
                    rgba(167,139,250,0.8) 90deg,
                    rgba(96,165,250,1) 180deg,
                    rgba(34,211,238,1) 270deg,
                    rgba(11, 19, 38, 0.1) 360deg
                );
                animation: borderSpinPseudo 4s linear infinite;
                z-index: 1;
                filter: drop-shadow(0 0 10px rgba(96,165,250,0.5));
            }
            
            /* The Inner Card Background (Masks the center of the gradient) */
            [st-key="auth_card"]::after {
                content: '';
                position: absolute;
                inset: 0px; /* Sit exactly inside the 2px border */
                background: #0b1326 !important; /* Dark solid background */
                border-radius: 22px;
                z-index: 2;
            }

            /* Container for the actual form content inside the card */
            [st-key="auth_card"] [data-testid="stVerticalBlock"] > div {
                position: relative;
                z-index: 3 !important; /* Above the inner background */
            }
            
            /* Apply padding to the inner content wrapper since we removed it from the border wrapper */
            [st-key="auth_card"] > [data-testid="stVerticalBlockBorderWrapper"] > div {
                 padding: 2.2rem !important;
            }

            @keyframes borderSpinPseudo {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes acPop {
                from { opacity:0; transform:scale(.92) translateY(22px); }
                to   { opacity:1; transform:scale(1) translateY(0); }
            }
            
            @keyframes authCardFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-8px); }
            }
            
            /* Center the right column */
            [data-testid="stColumn"]:last-of-type {
                display: flex !important; align-items: center !important; justify-content: center !important;
                perspective: 1200px; /* Add 3D perspective to right column */
                position: relative;
                z-index: 1;
            }
            
            /* ── Auth Column 3D Background Shapes ── */
            /* We inject these using st.markdown in python below */
            .right-scene-3d { position:absolute; inset:0; pointer-events:none; perspective:1000px; z-index:0; }
            
            .auth-orbital1 { position:absolute; top:12%; right:5%; width:80px; height:80px; transform-style:preserve-3d; animation:authRot1 25s linear infinite, authFloat1 12s ease-in-out infinite; }
            .auth-orbital1 .ring { position:absolute; width:100%; height:100%; border:2px solid rgba(167,139,250,.3); border-radius:50%; }
            .auth-orbital1 .r1 { transform: rotateX(65deg) rotateY(0deg); border-color: rgba(96,165,250,.4); }
            .auth-orbital1 .r2 { transform: rotateX(65deg) rotateY(60deg); border-color: rgba(167,139,250,.4); }
            .auth-orbital1 .r3 { transform: rotateX(65deg) rotateY(120deg); border-color: rgba(52,211,153,.4); }
            .auth-orbital1 .core { position:absolute; top:50%; left:50%; width:16px; height:16px; background:radial-gradient(circle, #60A5FA, transparent); border-radius:50%; transform:translate(-50%,-50%); box-shadow:0 0 15px rgba(96,165,250,.6); }
            
            .auth-orbital2 { position:absolute; bottom:10%; left:5%; width:55px; height:55px; transform-style:preserve-3d; animation:authRot2 18s linear infinite reverse, authFloat2 10s ease-in-out infinite; }
            .auth-orbital2 .ring { position:absolute; width:100%; height:100%; border:1.5px solid rgba(34,211,238,.3); border-radius:50%; }
            .auth-orbital2 .r1 { transform: rotateX(65deg) rotateY(0deg); }
            .auth-orbital2 .r2 { transform: rotateX(65deg) rotateY(60deg); border-color: rgba(59,130,246,.3); }
            .auth-orbital2 .r3 { transform: rotateX(65deg) rotateY(120deg); }
            .auth-orbital2 .core { position:absolute; top:50%; left:50%; width:10px; height:10px; background:radial-gradient(circle, #38BDF8, transparent); border-radius:50%; transform:translate(-50%,-50%); box-shadow:0 0 15px rgba(56,189,248,.5); }
            
            .auth-orb1 { position:absolute; top:25%; left:-5%; width:180px; height:180px; border-radius:50%; background:radial-gradient(circle, rgba(167,139,250,.12), transparent 70%); filter:blur(20px); animation:authOrbPulse 8s alternate infinite; }
            .auth-orb2 { position:absolute; bottom:15%; right:-5%; width:220px; height:220px; border-radius:50%; background:radial-gradient(circle, rgba(59,130,246,.1), transparent 70%); filter:blur(25px); animation:authOrbPulse 12s alternate infinite reverse; }
            
            @keyframes authRot1 { 0%{transform:rotateX(0) rotateY(0) rotateZ(0);} 100%{transform:rotateX(360deg) rotateY(-360deg) rotateZ(180deg);} }
            @keyframes authRot2 { 0%{transform:rotateX(45deg) rotateY(0);} 100%{transform:rotateX(45deg) rotateY(360deg);} }
            @keyframes authFloat1 { 0%,100%{top:12%;} 50%{top:8%;} }
            @keyframes authFloat2 { 0%,100%{bottom:10%;} 50%{bottom:15%;} }
            @keyframes authOrbPulse { 0%{transform:scale(0.8); opacity:0.5;} 100%{transform:scale(1.2); opacity:1;} }
            
            /* ── Tabs (via stRadio) ── */
            /* Hide the "Authentication Mode" label */
            [data-testid="stRadio"] > label,
            [data-testid="stRadio"] > div:first-child:not([role="radiogroup"]),
            div:has(> [data-testid="stRadio"]) > [data-testid="stWidgetLabel"],
            div:has(> div[role="radiogroup"]) > label,
            div:has(> [role="radiogroup"]) > label { display: none !important; height: 0 !important; overflow: hidden !important; margin: 0 !important; padding: 0 !important; }
            div:has(> div[data-testid="stRadio"]),
            div:has(> [data-testid="stRadio"]),
            [data-testid="stRadio"] { width: 100% !important; display: block !important; }
            
            [data-testid="stRadio"] > div[role="radiogroup"] { 
                display:flex !important; flex-direction:row !important; width: 100% !important; 
                background:rgba(255,255,255,.04) !important; border:1px solid rgba(255,255,255,.07) !important; 
                border-radius:10px !important; padding:4px !important; gap:4px !important; margin-bottom:1.8rem !important; 
            }
            [data-testid="stRadio"] label { 
                display: flex !important; align-items: center !important; justify-content: center !important;
                flex: 1 1 0% !important; width: 100% !important;
                padding:.6rem !important; border-radius:7px !important; font-size:.86rem !important; font-weight:600 !important;
                background:transparent !important; color:#64748B !important; text-align:center !important; transition:all .2s ease !important;
                cursor: pointer !important; margin: 0 !important; white-space: nowrap !important;
            }
            [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { display: none !important; } /* Hide circles */
            
            [data-testid="stRadio"] label:has(input:checked) { 
                background:linear-gradient(135deg, rgba(124,58,237,.9), rgba(59,130,246,.85)) !important; 
                box-shadow:0 2px 10px rgba(124,58,237,.4) !important; border:none !important;
            }
            [data-testid="stRadio"] label p { font-weight: 600 !important; font-size: 0.88rem !important; color: #64748B; margin: 0 !important;}
            [data-testid="stRadio"] label:has(input:checked) p { color:white !important; }
            
            /* ── Form header ── */
            .form-hdr { text-align:center; margin-bottom:1.8rem; }
            .form-ttl { 
                font-size:1.5rem; font-weight:800; letter-spacing:-.5px;
                background:linear-gradient(120deg,#E2E8F0 0%,#A78BFA 50%,#60A5FA 100%);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
                font-family:'Inter',sans-serif; margin-bottom:.3rem; 
            }
            .form-sub { font-size:.78rem; color:#64748B; font-family:'Inter',sans-serif; font-weight:400; }
            
            /* ── Form Inputs ── */
            [data-testid="stTextInput"] label p {
                font-size: 0.72rem !important; font-weight: 700 !important; color: #94A3B8 !important;
                letter-spacing: 0.6px !important; text-transform: uppercase !important; margin-bottom: 0.1rem !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"] {
                background-color: transparent !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"] > div {
                background-color: transparent !important;
                background: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(255, 255, 255, 0.09) !important;
                border-radius: 10px !important;
                transition: all 0.22s ease !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within > div {
                background: rgba(167, 139, 250, 0.07) !important; 
                border-color: rgba(167, 139, 250, 0.5) !important;
                box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.1), 0 0 14px rgba(167, 139, 250, 0.14) !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"] input {
                color: #F1F5F9 !important; font-size: 0.88rem !important;
                padding: 0.72rem 0.9rem 0.72rem 2.8rem !important;
                /* Default to User icon */
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='16' height='16' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important;
                background-repeat: no-repeat !important; background-position: 12px center !important;
            }
            [data-testid="stTextInput"] input::placeholder { color: #64748B !important; }
            
            /* Override to Lock icon for password type */
            [data-testid="stTextInput"] div[data-baseweb="input"] input[type="password"] {
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='16' height='16' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='11' width='18' height='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E") !important;
                background-repeat: no-repeat !important; background-position: 12px center !important;
            }
            
            /* Mail Icon */
            [data-testid="stTextInput"] div[data-baseweb="input"] input[placeholder="Enter your email address"] {
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='16' height='16' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z'/%3E%3Cpolyline points='22,6 12,13 2,6'/%3E%3C/svg%3E") !important;
                background-repeat: no-repeat !important; background-position: 12px center !important;
            }

            /* Password Eye Icon Mock (Streamlit has its own eye icon for type="password" but we can style the container if needed. Streamlit handles this natively so we leave it)*/
            
            /* ── Options row ── */
            .opt-row-st { display:flex; justify-content:space-between; align-items:center; margin:.5rem 0 1.3rem; font-family:'Inter',sans-serif; }
            .chk-label { display:flex; align-items:center; gap:6px; font-size:.78rem; color:#94A3B8; cursor:pointer; user-select:none; }
            .chk-label input[type="checkbox"] { 
                /* Custom styled checkbox matching exact look */
                appearance:none; -webkit-appearance:none; width:15px; height:15px; 
                border:1.5px solid rgba(255,255,255,.15); border-radius:4px; cursor:pointer; 
                position:relative; transition:all .2s;
            }
            .chk-label input[type="checkbox"]:checked {
                background: linear-gradient(135deg, #7C3AED, #3B82F6); border-color: #7C3AED;
            }
            .chk-label input[type="checkbox"]:checked::after {
                content: '✓'; position:absolute; top:45%; left:50%; transform:translate(-50%,-50%); 
                color:white; font-size:10px; font-weight:900;
            }
            .forgot-lnk { font-size:.78rem; color:#3B82F6; text-decoration:none; font-family:'Inter',sans-serif; }
            .forgot-lnk:hover { text-decoration:underline; }
            
            /* ── Sign In Button ── */
            /* Streamlit button comes inside a div. We target the button precisely */
            button[data-testid="baseButton-secondary"] {
                background: linear-gradient(135deg, #7C3AED, #3B82F6) !important;
                color: white !important; border: none !important; border-radius: 10px !important;
                padding: 0.75rem !important; font-weight: 600 !important; font-size: 0.95rem !important;
                width: 100% !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
                transition: all .2s ease !important;
            }
            button[data-testid="baseButton-secondary"]:hover {
                box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6) !important; transform: translateY(-1px) !important;
            }
            
            /* ── Alerts ── */
            .login-alert-err {
                background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.28);
                color:#FCA5A5; border-radius:9px; padding:.65rem .9rem; font-size:.82rem;
                font-weight:500; margin-bottom:.8rem; display:flex; align-items:center; gap:8px;
                font-family:'Inter',sans-serif; animation:fadeInAlert .3s ease; 
            }
            .login-alert-ok {
                background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.28);
                color:#34D399; border-radius:9px; padding:.65rem .9rem; font-size:.82rem;
                font-weight:500; margin-bottom:.8rem; display:flex; align-items:center; gap:8px;
                font-family:'Inter',sans-serif; animation:fadeInAlert .3s ease; 
            }
            .login-alert-ok::before {
                content: '✅'; font-size: 0.9rem;
            }
            @keyframes fadeInAlert { from{opacity:0;transform:translateY(-6px);} to{opacity:1;transform:translateY(0);} }
        </style>
        
        <div class="right-scene-3d">
            <div class="auth-orb1"></div>
            <div class="auth-orb2"></div>
            <div class="auth-orbital1"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
            <div class="auth-orbital2"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="core"></div></div>
        </div>
        """, unsafe_allow_html=True)

        # Wrap all form content in a keyed bordered container for CSS targeting
        with st.container(key='auth_card', border=True):
            # Tabs
            auth_mode = st.radio("Authentication Mode", ["Sign In", "Create Account"], horizontal=True, label_visibility="collapsed")
            
            if auth_mode == "Sign In":
                st.markdown("""
                <div class="form-hdr">
                    <div class="form-ttl">Welcome Back</div>
                    <div class="form-sub">Sign in to your academic dashboard</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Alerts
                if 'login_error' in st.session_state and st.session_state.login_error:
                    st.markdown(f'<div class="login-alert-err">⚠️ {st.session_state.login_error}</div>',
                                unsafe_allow_html=True)
                elif 'login_success' in st.session_state and st.session_state.login_success:
                    st.markdown(f'<div class="login-alert-ok">{st.session_state.login_success}</div>',
                                unsafe_allow_html=True)
                
                # Form fields
                username = st.text_input("Username or Email", placeholder="Enter your username",
                                         key="login_user", label_visibility="visible")
                password = st.text_input("Password", type="password", placeholder="Enter your password",
                                         key="login_pass", label_visibility="visible")
                
                # Remember me + Forgot password
                st.markdown("""
                <div class="opt-row-st">
                    <label class="chk-label"><input type="checkbox"> Remember me</label>
                    <a href="#" class="forgot-lnk">Forgot password?</a>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Sign In  →", key="login_submit", use_container_width=True):
                    if not username:
                        st.session_state.login_error = "Please enter your username or email."
                        st.rerun()
                    elif not password:
                        st.session_state.login_error = "Please enter your password."
                        st.rerun()
                    else:
                        # 4 default credentials + any registered accounts
                        default_users = {
                            "admin": "admin123",
                            "sathish": "sathish123",
                            "student": "student123",
                            "teacher": "teacher123",
                        }
                        registered = st.session_state.get('registered_users', {})
                        # Merge: defaults + registered
                        all_users = {**default_users, **registered}
                        
                        if username in all_users and all_users[username] == password:
                            st.session_state.login_error = None
                            st.session_state.login_success = None
                            st.session_state.authenticated = True
                            st.session_state.logged_in_user = username
                            st.session_state.just_logged_in = True
                            st.rerun()
                        else:
                            st.session_state.login_error = "Invalid username or password."
                            st.rerun()
                        
            else:
                # Create Account UI
                st.markdown("""
                <div class="form-hdr">
                    <div class="form-ttl">Create Account</div>
                    <div class="form-sub">Join the analytics platform</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Alerts
                if 'register_error' in st.session_state and st.session_state.register_error:
                    st.markdown(f'<div class="login-alert-err">⚠️ {st.session_state.register_error}</div>', unsafe_allow_html=True)
                
                # Form fields
                new_fullname = st.text_input("Full Name", placeholder="Enter your full name", key="create_name")
                new_username = st.text_input("Username", placeholder="Choose a username", key="create_username")
                new_email = st.text_input("Email Address", placeholder="Enter your email address", key="create_email")
                new_password = st.text_input("Password", type="password", placeholder="Create a password", key="create_pass")
                
                # Terms
                st.markdown("""
                <div class="opt-row-st" style="margin-top:0.8rem; margin-bottom: 1.5rem;">
                    <label class="chk-label"><input type="checkbox" checked> I agree to the Terms & Conditions</label>
                </div>
                """, unsafe_allow_html=True)
                
                # Registration success alert
                if 'register_success' in st.session_state and st.session_state.register_success:
                    st.markdown(f'<div class="login-alert-ok">{st.session_state.register_success}</div>', unsafe_allow_html=True)
                
                if st.button("Create Account  →", key="create_submit", use_container_width=True):
                    if not new_fullname or not new_username or not new_email or not new_password:
                        st.session_state.register_error = "All fields are required to create an account."
                        st.session_state.register_success = None
                        st.rerun()
                    else:
                        # Store registration in session state
                        if 'registered_users' not in st.session_state:
                            st.session_state.registered_users = {}
                        st.session_state.registered_users[new_username] = new_password
                        st.session_state.register_error = None
                        st.session_state.register_success = f"Account created successfully! Sign in with username '{new_username}'."
                        st.session_state.login_success = f"Account created! Please sign in with your credentials."
                        st.rerun()


if __name__ == "__main__":
    if st.session_state.authenticated:
        main()
    else:
        render_login_page()



