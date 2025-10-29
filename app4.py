import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta
import calendar

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Smart Leave System - SNSCT", page_icon="🤖", layout="wide")

# ------------------- SESSION STATE -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user" not in st.session_state:
    st.session_state.user = None
if "attendance" not in st.session_state:
    st.session_state.attendance = 100  # default attendance

# ------------------- BACKGROUND STYLE -------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(135deg, #e8f0ff 0%, #d7e1fa 100%);
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------- RANDOM LOGO -------------------
logos = [
    "https://upload.wikimedia.org/wikipedia/commons/1/19/SNS_College_of_Technology_logo.png",
    "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
    "https://cdn-icons-png.flaticon.com/512/1053/1053244.png"
]
logo_url = random.choice(logos)

# ------------------- LOGIN PAGE -------------------
def login_page():
    st.image(logo_url, width=120)
    st.title("🔐 Smart Leave Login - SNS COLLEGE OF TECHNOLOGY")
    st.markdown("### Please log in to continue")

    role = st.radio("Login as", ["Student", "Teacher"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if role == "Student" and username == "student" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.role = "student"
            st.session_state.user = username
        elif role == "Teacher" and username == "teacher" and password == "admin":
            st.session_state.logged_in = True
            st.session_state.role = "teacher"
            st.session_state.user = username
        else:
            st.error("Invalid credentials! Use student/1234 or teacher/admin")

    st.markdown("---")
    st.info("🧑‍🎓 Student Login → `student / 1234`\n🧑‍🏫 Teacher Login → `teacher / admin`")

# ------------------- STUDENT DASHBOARD -------------------
def student_dashboard():
    st.image(logo_url, width=120)
    st.title("🎓 Student Dashboard - SNS COLLEGE OF TECHNOLOGY")
    st.write(f"Welcome, **{st.session_state.user}** 👋")
    st.progress(st.session_state.attendance / 100)
    st.write(f"📊 Current Attendance: **{st.session_state.attendance}%**")

    tab1, tab2, tab3 = st.tabs(["📝 Apply Leave", "📅 Calendar", "📄 Leave Letter"])

    # ---- APPLY LEAVE ----
    with tab1:
        st.subheader("Apply for Leave")
        reason = st.selectbox("Reason", ["Medical", "Personal", "Other"])
        from_date = st.date_input("From Date", value=date.today())
        to_date = st.date_input("To Date", value=date.today())

        days = (to_date - from_date).days + 1

        if st.button("Submit Leave"):
            # Attendance deduction logic
            if st.session_state.attendance < 75:
                st.warning("⚠️ Attendance below 75%! Not recommended to take leave.")
                status = "Rejected"
            else:
                st.session_state.attendance -= days * 3
                if st.session_state.attendance < 0:
                    st.session_state.attendance = 0

                if reason == "Medical":
                    status = "Approved"
                elif st.session_state.attendance > 85:
                    status = "Approved"
                else:
                    status = "Pending"

            st.session_state.leave_status = status
            st.session_state.leave_dates = (from_date, to_date)

            color = (
                "green"
                if status == "Approved"
                else "red"
                if status == "Rejected"
                else "orange"
            )
            st.markdown(f"### Decision: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
            st.success(f"Your updated attendance is {st.session_state.attendance}%")

    # ---- CALENDAR ----
    with tab2:
        st.subheader("📅 Attendance Calendar")
        today = date.today()
        year, month = today.year, today.month
        cal = calendar.Calendar()
        days_in_month = cal.itermonthdates(year, month)
        st.write(f"### {calendar.month_name[month]} {year}")

        cols = st.columns(7)
        for i, day in enumerate(days_in_month):
            col = cols[i % 7]
            if day.month == month:
                color = "#90EE90" if "leave_status" in st.session_state and st.session_state.leave_status == "Approved" and st.session_state.leave_dates[0] <= day <= st.session_state.leave_dates[1] else \
                        "#FF7F7F" if "leave_status" in st.session_state and st.session_state.leave_status == "Rejected" and st.session_state.leave_dates[0] <= day <= st.session_state.leave_dates[1] else "#F8F9FA"
                col.markdown(f"<div style='background:{color};padding:8px;border-radius:8px;text-align:center'>{day.day}</div>", unsafe_allow_html=True)

    # ---- LEAVE LETTER PREVIEW ----
    with tab3:
        st.subheader("📄 Leave Letter Preview")

        if "leave_status" in st.session_state:
            leave_letter = f"""
--------------------------------------------------
                SNS COLLEGE OF TECHNOLOGY
--------------------------------------------------

Student Name : {st.session_state.user}
Department    : CSE
Date          : {date.today().strftime('%d-%m-%Y')}

Subject: Leave Application

Respected Sir/Madam,

I request leave from {st.session_state.leave_dates[0]} to {st.session_state.leave_dates[1]}
due to {reason} reasons.

Kindly approve my leave.

Status: {st.session_state.leave_status}

Regards,
{st.session_state.user}
--------------------------------------------------
            """
            st.markdown(f"""
            <div style='background-color:#fff; padding:20px; border-radius:10px;
                        box-shadow:0 4px 10px rgba(0,0,0,0.15); font-family:monospace;
                        white-space:pre-wrap; color:#000;'>
            {leave_letter}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No leave record found to display.")

# ------------------- TEACHER DASHBOARD -------------------
def teacher_dashboard():
    st.image(logo_url, width=120)
    st.title("🧑‍🏫 Teacher Dashboard - SNS COLLEGE OF TECHNOLOGY")
    st.write("View and manage student leave requests")

    dummy_data = pd.DataFrame({
        "Student": ["student1", "student2", "student3"],
        "Reason": ["Medical", "Personal", "Other"],
        "From": ["2025-10-25", "2025-10-26", "2025-10-27"],
        "To": ["2025-10-26", "2025-10-27", "2025-10-28"],
        "Status": ["Pending", "Approved", "Pending"]
    })

    edited = st.data_editor(dummy_data, num_rows="dynamic")
    st.success("Changes saved automatically (demo mode).")

# ------------------- MAIN -------------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "student":
        student_dashboard()
    else:
        teacher_dashboard()
