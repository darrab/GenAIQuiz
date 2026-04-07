import streamlit as st
import random
import json
import time
from datetime import datetime, timedelta
import hashlib
import os

# ==========================
# CONFIG
# ==========================
st.set_page_config(page_title="AI Quiz Pro", layout="wide")

DATA_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"

# ==========================
# UTILS
# ==========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# ==========================
# AUTH SYSTEM
# ==========================
def login_signup():
    st.sidebar.title("🔐 Login")

    users = load_json(DATA_FILE)

    choice = st.sidebar.radio("Choose", ["Login", "Sign Up"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.sidebar.button("Create Account"):
            if username in users:
                st.sidebar.error("User exists!")
            else:
                users[username] = hash_password(password)
                save_json(DATA_FILE, users)
                st.sidebar.success("Account created!")

    if choice == "Login":
        if st.sidebar.button("Login"):
            if username in users and users[username] == hash_password(password):
                st.session_state.user = username
                st.sidebar.success(f"Welcome {username}")
            else:
                st.sidebar.error("Invalid credentials")

# ==========================
# FIX ANSWERS AUTOMATICALLY
# ==========================
def fix_answers(questions):
    for q in questions:
        correct = None
        for opt in q["opts"]:
            if q["exp"].lower() in opt.lower():
                correct = opt[0]
        if correct:
            q["ans"] = correct
        else:
            q["ans"] = q["ans"] if q["ans"] in ["A","B","C","D"] else "B"
    return questions

# ==========================
# LOAD QUESTIONS
# ==========================
with open('questions.json', 'r') as f:
    QUESTIONS = json.load(f)

# ==========================
# SESSION INIT
# ==========================
def init_state():
    defaults = {
        "quiz_started": False,
        "current_q": 0,
        "score": 0,
        "answers": {},
        "selected_questions": [],
        "mode": None,
        "start_time": None,
        "duration": 0,
        "submitted": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ==========================
# LEADERBOARD
# ==========================
def update_leaderboard(user, score):
    data = load_json(LEADERBOARD_FILE)
    data[user] = max(score, data.get(user, 0))
    save_json(LEADERBOARD_FILE, data)

def show_leaderboard():
    st.sidebar.subheader("🏆 Leaderboard")
    data = load_json(LEADERBOARD_FILE)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    for user, score in sorted_data[:10]:
        st.sidebar.write(f"**{user}**: {score}")

# ==========================
# QUIZ SETUP
# ==========================
def setup_quiz():
    st.sidebar.title("⚙️ Settings")

    mode = st.sidebar.radio("Mode", ["Practice", "Exam"])

    lectures = list(set(q["lec"] for q in QUESTIONS))
    selected_lectures = st.sidebar.multiselect("Lectures", lectures, default=lectures)

    num_q = st.sidebar.slider("Questions", 5, 50, 10)

    duration = 0
    if mode == "Exam":
        duration = st.sidebar.slider("Time (minutes)", 1, 60, 10)

    if st.sidebar.button("Start Quiz"):
        filtered = [q for q in QUESTIONS if q["lec"] in selected_lectures]
        st.session_state.selected_questions = random.sample(filtered, num_q)

        st.session_state.mode = mode
        st.session_state.quiz_started = True
        st.session_state.start_time = datetime.now()
        st.session_state.duration = duration

# ==========================
# TIMER
# ==========================
def show_timer():
    if st.session_state.mode == "Exam":
        elapsed = datetime.now() - st.session_state.start_time
        remaining = timedelta(minutes=st.session_state.duration) - elapsed

        if remaining.total_seconds() <= 0:
            st.session_state.submitted = True
            st.warning("⏰ Time's up!")
        else:
            st.sidebar.write(f"⏱ Time left: {str(remaining).split('.')[0]}")

# ==========================
# QUIZ UI
# ==========================
def handle_answer():
    q_idx = st.session_state.current_q
    key = f"q_{q_idx}"

    # Prevent re-submission
    if q_idx in st.session_state.answers:
        return

    selected_option = st.session_state[key]
    selected_letter = selected_option[0]

    st.session_state.answers[q_idx] = selected_letter

    if selected_letter == st.session_state.selected_questions[q_idx]["ans"]:
        st.session_state.score += 1


def show_question():
    q_idx = st.session_state.current_q
    q = st.session_state.selected_questions[q_idx]

    st.markdown(f"### Q{q_idx+1}: {q['q']}")

    key = f"q_{q_idx}"

    # If already answered → disable radio
    disabled = q_idx in st.session_state.answers

    st.radio(
        "Options",
        q["opts"],
        key=key,
        on_change=handle_answer,
        disabled=disabled
    )

    # ==========================
    # PRACTICE MODE FEEDBACK
    # ==========================
    if st.session_state.mode == "Practice" and q_idx in st.session_state.answers:
        selected = st.session_state.answers[q_idx]

        if selected == q["ans"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Correct Answer: {q['ans']}")

        st.info(f"💡 {q['exp']}")

    # ==========================
    # NAVIGATION
    # ==========================
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Previous") and q_idx > 0:
            st.session_state.current_q -= 1

    with col2:
        if st.button("Next ➡️"):
            if q_idx < len(st.session_state.selected_questions) - 1:
                st.session_state.current_q += 1
            else:
                st.session_state.submitted = True

# ==========================
# RESULTS
# ==========================
def show_results():
    total = len(st.session_state.selected_questions)

    st.title("📊 Results")
    st.metric("Score", f"{st.session_state.score}/{total}")

    if "user" in st.session_state:
        update_leaderboard(st.session_state.user, st.session_state.score)

    st.subheader("Review Mistakes")

    for i, q in enumerate(st.session_state.selected_questions):
        if st.session_state.answers.get(i) != q["ans"]:
            st.write(f"Q: {q['q']}")
            st.write(f"Your: {st.session_state.answers.get(i)} | Correct: {q['ans']}")
            st.info(q["exp"])
            st.divider()

# ==========================
# MAIN
# ==========================
login_signup()

if "user" in st.session_state:
    show_leaderboard()
    setup_quiz()
    show_timer()

    if not st.session_state.quiz_started:
        st.info("Start a quiz from sidebar")

    elif st.session_state.submitted:
        show_results()

    else:
        show_question()
else:
    st.warning("Please login to continue")
