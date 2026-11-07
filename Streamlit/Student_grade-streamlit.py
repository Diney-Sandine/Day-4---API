import html

import streamlit as st

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(page_title="Student Grade Manager", page_icon="🎓", layout="wide")

# ------------------------------------------------------------------
# Styling: light background + dark text everywhere, so every word is
# clearly visible regardless of the user's Streamlit theme.
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 50%, #ecfeff 100%);
    }
    /* Force dark, readable text on all common elements */
    .stApp, .stApp p, .stApp label, .stApp span, .stApp li,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
    }
    header[data-testid="stHeader"] { background: transparent; }

    /* Hero banner */
    .hero {
        background: linear-gradient(120deg, #4338ca, #0891b2);
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(67, 56, 202, 0.25);
    }
    .hero h1, .hero p { color: #ffffff !important; margin: 0; }
    .hero h1 { font-size: 2.2rem; font-weight: 800; }
    .hero p  { font-size: 1.05rem; margin-top: 6px; opacity: 0.95; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #c7d2fe;
        border-left: 6px solid #4338ca;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    }
    [data-testid="stMetricLabel"] p {
        color: #334155 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    /* Section cards */
    .section-title {
        font-size: 1.35rem; font-weight: 800; color: #1e1b4b !important;
        margin: 26px 0 10px 0;
    }

    /* Form container */
    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #c7d2fe;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }

    /* Buttons */
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: #4338ca; color: #ffffff !important; font-weight: 700;
        border: none; border-radius: 10px; padding: 0.55rem 1.2rem;
    }
    .stButton > button p, [data-testid="stFormSubmitButton"] > button p {
        color: #ffffff !important;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background: #3730a3;
    }

    /* Custom HTML table */
    table.grades {
        width: 100%; border-collapse: collapse; background: #ffffff;
        border-radius: 14px; overflow: hidden;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        font-size: 1.05rem;
    }
    table.grades th {
        background: #1e1b4b; color: #ffffff !important; text-align: left;
        padding: 14px 18px; font-weight: 700;
    }
    table.grades td {
        color: #0f172a !important; padding: 12px 18px;
        border-bottom: 1px solid #e2e8f0;
    }
    table.grades tr:nth-child(even) td { background: #f1f5f9; }
    .badge {
        display: inline-block; min-width: 36px; text-align: center;
        padding: 4px 12px; border-radius: 999px; font-weight: 800;
        color: #ffffff !important;
    }
    .A { background: #15803d; } .B { background: #0369a1; }
    .C { background: #b45309; } .D { background: #c2410c; }
    .F { background: #b91c1c; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def get_grade(mark: float) -> str:
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


# ------------------------------------------------------------------
# Session state: the student list survives reruns
# ------------------------------------------------------------------
if "students" not in st.session_state:
    st.session_state.students = [
        {"name": "Aarav", "mark": 92.0},
        {"name": "Meera", "mark": 78.5},
        {"name": "Karthik", "mark": 85.0},
    ]

students = st.session_state.students

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎓 Student Grade Manager</h1>
        <p>Add students, track marks and see class statistics at a glance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Class statistics (metrics)
# ------------------------------------------------------------------
st.markdown('<div class="section-title">📊 Class Statistics</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
if students:
    marks = [s["mark"] for s in students]
    top = max(students, key=lambda s: s["mark"])
    low = min(students, key=lambda s: s["mark"])
    m1.metric("Total Students", len(students))
    m2.metric("Class Average", f"{sum(marks) / len(marks):.1f}")
    m3.metric("Highest Mark", f"{top['mark']:.1f}", top["name"], delta_color="off")
    m4.metric("Lowest Mark", f"{low['mark']:.1f}", low["name"], delta_color="off")
else:
    m1.metric("Total Students", 0)
    m2.metric("Class Average", "–")
    m3.metric("Highest Mark", "–")
    m4.metric("Lowest Mark", "–")

# ------------------------------------------------------------------
# Add student form
# ------------------------------------------------------------------
st.markdown('<div class="section-title">➕ Add a Student</div>', unsafe_allow_html=True)

with st.form("add_student_form", clear_on_submit=True):
    c1, c2 = st.columns([2, 1])
    name = c1.text_input("Student name", placeholder="e.g. Priya")
    mark = c2.number_input("Mark (0 - 100)", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
    submitted = st.form_submit_button("Add Student")

if submitted:
    clean_name = name.strip()
    if not clean_name:
        st.error("Please enter a student name.")
    elif any(s["name"].lower() == clean_name.lower() for s in students):
        st.warning(f"'{clean_name}' is already in the list. Remove them first to re-enter.")
    else:
        students.append({"name": clean_name, "mark": float(mark)})
        st.success(f"Added {clean_name} with {mark:.1f} marks (Grade {get_grade(mark)}).")
        st.rerun()

# ------------------------------------------------------------------
# Student table
# ------------------------------------------------------------------
st.markdown('<div class="section-title">📋 All Students</div>', unsafe_allow_html=True)

if students:
    rows = ""
    for i, s in enumerate(students, start=1):
        g = get_grade(s["mark"])
        rows += (
            f"<tr><td>{i}</td><td>{html.escape(s['name'])}</td>"
            f"<td>{s['mark']:.1f}</td>"
            f"<td><span class='badge {g}'>{g}</span></td></tr>"
        )
    st.markdown(
        f"""
        <table class="grades">
            <thead><tr><th>#</th><th>Name</th><th>Mark</th><th>Grade</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    # Remove a student
    st.markdown('<div class="section-title">🗑️ Remove a Student</div>', unsafe_allow_html=True)
    r1, r2 = st.columns([2, 1])
    to_remove = r1.selectbox("Choose a student", [s["name"] for s in students])
    r2.write("")
    r2.write("")
    if r2.button("Remove Student"):
        st.session_state.students = [s for s in students if s["name"] != to_remove]
        st.rerun()
else:
    st.info("No students yet. Add one using the form above.")

st.markdown(
    "<p style='margin-top:28px;'><b>Grading scale:</b> A ≥ 90 · B ≥ 80 · C ≥ 70 · D ≥ 60 · F &lt; 60</p>",
    unsafe_allow_html=True,
)