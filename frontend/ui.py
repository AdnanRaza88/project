import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Grade Tracker", layout="wide")

st.markdown("""
<head>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            background: #eef0f2;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        .neumorphic-card {
            background: #eef0f2;
            border-radius: 40px;
            box-shadow: 12px 12px 24px #b8b9be, -12px -12px 24px #ffffff;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: 0.2s;
        }
        .neumorphic-button {
            background: #eef0f2;
            border: none;
            border-radius: 60px;
            box-shadow: 6px 6px 12px #b8b9be, -6px -6px 12px #ffffff;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            color: #1e2a3e;
            cursor: pointer;
            transition: 0.1s;
        }
        .neumorphic-button:active {
            box-shadow: inset 6px 6px 12px #b8b9be, inset -6px -6px 12px #ffffff;
        }
        .question-block {
            background: #ffffffcc;
            backdrop-filter: blur(4px);
            border-radius: 28px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem;
            font-size: 0.85rem;
            color: #4a5568;
            border-top: 1px solid #cbd5e1;
        }
        .percentage-slider {
            background: white;
            border-radius: 60px;
            padding: 0.5rem 1rem;
            margin: 1rem 0;
        }
        h1, h2, h3 {
            color: #0f172a;
            font-weight: 600;
        }
    </style>
</head>
""", unsafe_allow_html=True)

st.markdown("""
<div class="neumorphic-card" style="text-align: center;">
    <h1 style="font-size: 2.2rem;">Student Grade Tracker</h1>
    <p style="color: #334155;">Track, analyze, and improve with AI assistance</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="question-block">
    <p style="font-weight: bold; font-size: 1.2rem;">Boost Your Learning</p>
    <ul style="list-style-type: none; padding-left: 0;">
        <li><strong>Follow this step – you learn full book in 1 month?</strong> <span style="color:#2563eb;">(Click AI Study Tips)</span></li>
        <li><strong>Struggling with focus? Click for secret technique.</strong></li>
        <li><strong>Improve 20% marks in 7 days – possible?</strong></li>
    </ul>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("Navigation", ["Add Record", "View All", "View One", "Update Record", "Delete Record", "AI Study Tips", "Motivation Quote", "Improvement Plan"])

def percentage_slider(marks, total):
    if total > 0:
        perc = (marks / total) * 100
        st.markdown(f"<div class='percentage-slider'>Percentage: {perc:.1f}%</div>", unsafe_allow_html=True)
        st.slider(" ", 0.0, 100.0, perc, disabled=True, key="perc_slider")

if menu == "Add Record":
    st.markdown("<div class='neumorphic-card'><h2>Add New Grade</h2>", unsafe_allow_html=True)
    with st.form("add"):
        name = st.text_input("Student Name")
        subject = st.text_input("Subject")
        marks = st.number_input("Marks Obtained", min_value=0.0, step=0.5)
        total = st.number_input("Total Marks", min_value=1.0, step=0.5)
        semester = st.text_input("Semester")
        date = st.date_input("Date")
        if marks and total:
            percentage_slider(marks, total)
        submitted = st.form_submit_button("Save Record")
        if submitted:
            if not name or not subject or not semester:
                st.error("Please fill all fields")
            else:
                payload = {
                    "student_name": name,
                    "subject": subject,
                    "marks_obtained": marks,
                    "total_marks": total,
                    "semester": semester,
                    "date": str(date)
                }
                resp = requests.post(f"{API_URL}/grades", json=payload)
                if resp.status_code == 201:
                    st.success("Record saved successfully")
                else:
                    st.error(f"Error: {resp.text}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "View All":
    st.markdown("<div class='neumorphic-card'><h2>All Grade Records</h2>", unsafe_allow_html=True)
    resp = requests.get(f"{API_URL}/grades")
    if resp.status_code == 200:
        data = resp.json()
        if data:
            st.dataframe(data)
        else:
            st.info("No records found.")
    else:
        st.error("Could not fetch data.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "View One":
    st.markdown("<div class='neumorphic-card'><h2>Find a Record</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID", min_value=1, step=1)
    if st.button("Search"):
        resp = requests.get(f"{API_URL}/grades/{gid}")
        if resp.status_code == 200:
            st.json(resp.json())
        else:
            st.warning("Record not found")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Update Record":
    st.markdown("<div class='neumorphic-card'><h2>Update Existing Record</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID to Update", min_value=1, step=1)
    with st.form("update"):
        name = st.text_input("Student Name")
        subject = st.text_input("Subject")
        marks = st.number_input("Marks Obtained", min_value=0.0, step=0.5)
        total = st.number_input("Total Marks", min_value=1.0, step=0.5)
        semester = st.text_input("Semester")
        date = st.date_input("Date")
        if marks and total:
            percentage_slider(marks, total)
        submitted = st.form_submit_button("Update")
        if submitted:
            payload = {
                "student_name": name,
                "subject": subject,
                "marks_obtained": marks,
                "total_marks": total,
                "semester": semester,
                "date": str(date)
            }
            resp = requests.put(f"{API_URL}/grades/{gid}", json=payload)
            if resp.status_code == 200:
                st.success("Updated successfully")
            else:
                st.error("Update failed - ID might not exist")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Delete Record":
    st.markdown("<div class='neumorphic-card'><h2>Delete Record</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID to Delete", min_value=1, step=1)
    if st.button("Permanently Delete"):
        resp = requests.delete(f"{API_URL}/grades/{gid}")
        if resp.status_code == 200:
            st.success("Deleted successfully")
        else:
            st.error("Delete failed - ID not found")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "AI Study Tips":
    st.markdown("<div class='neumorphic-card'><h2>Personalized AI Study Tips</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID", min_value=1, step=1, key="tips_id")
    challenges = st.selectbox("What's your biggest challenge?", ["Understanding concepts", "Memorization", "Time management", "Exam pressure", "Lack of focus"])
    study_hours = st.selectbox("Daily study hours", ["<1 hour", "1-2 hours", "3-4 hours", "5+ hours"])
    exam_fear = st.selectbox("Do you feel nervous before exams?", ["Yes, very much", "A little", "Not at all"])
    if st.button("Get Study Tips"):
        resp = requests.post(f"{API_URL}/grades/{gid}/study-tips", params={"challenges": challenges, "study_hours": study_hours, "exam_fear": exam_fear})
        if resp.status_code == 200:
            tips = resp.json()["study_tips"]
            st.success(tips)
        else:
            st.error("Record not found")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Motivation Quote":
    st.markdown("<div class='neumorphic-card'><h2>AI Motivation Quote</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID", min_value=1, step=1, key="mot_id")
    if st.button("Get Motivated"):
        resp = requests.post(f"{API_URL}/grades/{gid}/motivation")
        if resp.status_code == 200:
            st.info(resp.json()["motivation_quote"])
        else:
            st.error("Record not found")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Improvement Plan":
    st.markdown("<div class='neumorphic-card'><h2>7-Day AI Improvement Plan</h2>", unsafe_allow_html=True)
    gid = st.number_input("Grade ID", min_value=1, step=1, key="plan_id")
    if st.button("Generate Plan"):
        resp = requests.post(f"{API_URL}/grades/{gid}/improvement-plan")
        if resp.status_code == 200:
            st.markdown(f"<div style='background:#f1f5f9; padding:1rem; border-radius:1rem;'>{resp.json()['improvement_plan']}</div>", unsafe_allow_html=True)
        else:
            st.error("Record not found")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<footer>
    <hr>
    Created by <strong>AdnanRaza</strong><br>
    WhatsApp: +923460364932 | Gmail: adnanrazaar786@gmail.com
</footer>
""", unsafe_allow_html=True)