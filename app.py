import streamlit as st
import random
import time
from datetime import datetime, timedelta
import json

# ==============================================================================
# QUESTION DATABASE (300 Questions - 50 per Lecture)
# ==============================================================================

try:
    with open('questions.json', 'r', encoding='utf-8') as f:
        QUESTIONS = json.load(f)
    print(f"✅ Successfully loaded {len(QUESTIONS)} questions")
except json.JSONDecodeError as e:
    print(f"❌ JSON Error at line {e.lineno}, column {e.colno}: {e.msg}")
    print(f"Check around character position: {e.pos}")
    # Show the problematic section
    with open('questions.json', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if e.lineno <= len(lines):
            print(f"Problematic line {e.lineno}: {lines[e.lineno-1][:100]}")
    raise

# ==============================================================================
# STREAMLIT APP - ENHANCED VERSION
# ==============================================================================

st.set_page_config(
    page_title="Deep Learning Quiz Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
    }
    .question-counter {
        font-size: 1.2rem;
        font-weight: bold;
        color: #424242;
        background: #E3F2FD;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    .timer-box {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFFFFF;
        background: #F44336;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    .timer-warning {
        background: #FF9800;
    }
    .timer-danger {
        background: #F44336;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .question-nav {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    .flagged {
        border: 2px solid #FF9800;
        background: #FFF3E0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'selected_lecture' not in st.session_state:
    st.session_state.selected_lecture = "All"
if 'timer_enabled' not in st.session_state:
    st.session_state.timer_enabled = False
if 'time_limit' not in st.session_state:
    st.session_state.time_limit = 30  # minutes
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'flagged_questions' not in st.session_state:
    st.session_state.flagged_questions = set()
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = "practice"  # practice or exam

# Helper functions
def format_time(seconds):
    """Format seconds as MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def get_timer_color(time_left, total_time):
    """Get timer color based on remaining time"""
    if time_left <= 0:
        return "timer-danger"
    elif time_left < total_time * 0.2:
        return "timer-danger"
    elif time_left < total_time * 0.4:
        return "timer-warning"
    return ""


def init_quiz(lecture_selection, time_limit_minutes, mode):
    """Initialize quiz with selected parameters"""
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.show_result = False
    st.session_state.selected_lecture = lecture_selection
    st.session_state.time_limit = time_limit_minutes
    st.session_state.quiz_mode = mode
    st.session_state.flagged_questions = set()
    
    # Filter questions
    if lecture_selection == "All":
        st.session_state.quiz_questions = QUESTIONS.copy()
    else:
        lec_num = int(lecture_selection.split()[1])
        st.session_state.quiz_questions = [q for q in QUESTIONS if q['lec'] == lec_num]
    
    # Shuffle questions
    random.shuffle(st.session_state.quiz_questions)
    
    # Set start time
    if st.session_state.timer_enabled:
        st.session_state.start_time = datetime.now()

# Sidebar
with st.sidebar:
    st.title("🎓 Quiz Settings")
    st.markdown("---")
    
    # Lecture Selection
    lecture_options = ["All"] + [f"Lecture {i:02d}" for i in range(1, 7)]
    selected_lecture = st.selectbox(
        "📚 Select Lecture:",
        lecture_options,
        index=0
    )
    
    # Timer Settings
    st.markdown("### ⏱️ Timer Settings")
    timer_enabled = st.checkbox("Enable Timer", value=False)
    
    if timer_enabled:
        time_limit = st.selectbox(
            "Time Limit:",
            [10, 15, 20, 30, 45, 60],
            index=3  # Default 30 minutes
        )
        st.session_state.timer_enabled = True
        st.session_state.time_limit = time_limit
    else:
        st.session_state.timer_enabled = False
    
    # Quiz Mode
    st.markdown("### 🎯 Quiz Mode")
    quiz_mode = st.radio(
        "Select Mode:",
        ["Practice", "Exam"],
        help="Practice: Show answers immediately. Exam: Show results at end."
    )
    
    st.markdown("---")
    
    # Action Buttons
    if st.button("🚀 Start New Quiz", type="primary", use_container_width=True):
        init_quiz(selected_lecture, st.session_state.time_limit, quiz_mode.lower())
        st.rerun()
    
    if st.button("📊 View Summary", disabled=not st.session_state.quiz_started, use_container_width=True):
        st.session_state.show_result = True
        st.rerun()
    
    if st.button("🏠 Reset Quiz", use_container_width=True):
        st.session_state.quiz_started = False
        st.session_state.show_result = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📈 Statistics")
    st.metric("Total Questions", len(QUESTIONS))
    if st.session_state.quiz_started:
        st.metric("Quiz Questions", len(st.session_state.quiz_questions))
        answered = len(st.session_state.answers)
        st.metric("Answered", f"{answered}/{len(st.session_state.quiz_questions)}")
    
    # Flagged Questions
    if st.session_state.flagged_questions:
        st.markdown("### 🚩 Flagged Questions")
        for q_num in sorted(st.session_state.flagged_questions):
            st.write(f"• Question {q_num + 1}")

# Main Content
st.markdown('<p class="main-header">🎓 Deep Learning & Gen AI Quiz Master</p>', unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.quiz_started:
    # Welcome Screen
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Questions", "300")
    with col2:
        st.metric("📖 Lectures", "6")
    with col3:
        st.metric("✅ Passing Score", "60%")
    
    st.markdown("""
    ### 📋 Quiz Features
    
    | Feature | Description |
    |---------|-------------|
    | ⏱️ **Timer** | Optional countdown timer (10-60 minutes) |
    | 📊 **Question Counter** | Track progress (e.g., 15/50) |
    | ⬅️➡️ **Navigation** | Move between questions freely |
    | 🚩 **Flag Questions** | Mark questions for review |
    | 📝 **Two Modes** | Practice (instant feedback) or Exam (results at end) |
    | 📈 **Progress Bar** | Visual progress indicator |
    | 📊 **Question Grid** | Jump to any question quickly |
    | 💾 **Auto-save** | Answers saved automatically |
    | 📤 **Export Results** | Download results as CSV |
    
    ### 🎯 How to Use
    
    1. **Select Lecture** - Choose specific lecture or all
    2. **Enable Timer** (optional) - Set time limit
    3. **Choose Mode** - Practice or Exam
    4. **Start Quiz** - Begin answering questions
    5. **Navigate** - Use Previous/Next buttons
    6. **Submit** - View results when done
    """)
    
    st.info("💡 **Tip:** Use Practice mode for learning, Exam mode for testing!")
    
else:
    questions = st.session_state.quiz_questions
    total_questions = len(questions)
    
    # Timer Display
    if st.session_state.timer_enabled and st.session_state.start_time:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        total_seconds = st.session_state.time_limit * 60
        time_left = max(0, total_seconds - elapsed)
        
        timer_class = get_timer_color(time_left, total_seconds)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"**Quiz Mode:** {st.session_state.quiz_mode.title()}")
        with col2:
            st.markdown(f'<p class="timer-box {timer_class}">⏱️ {format_time(int(time_left))}</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f"**Lecture:** {st.session_state.selected_lecture}")
        
        if time_left <= 0:
            st.error("⏰ Time's up! Submitting your answers...")
            st.session_state.show_result = True
            st.rerun()
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Quiz Mode:** {st.session_state.quiz_mode.title()}")
        with col2:
            st.markdown(f"**Lecture:** {st.session_state.selected_lecture}")
    
    st.markdown("---")
    
    if st.session_state.show_result:
        # Results Page
        st.markdown("## 📊 Quiz Results")
        
        # Calculate score
        correct_count = 0
        for q_idx, answer_data in st.session_state.answers.items():
            if q_idx < len(questions):
                if answer_data.get('answer') == questions[q_idx]['ans']:
                    correct_count += 1
        
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Score Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Correct", correct_count)
        with col3:
            st.metric("Incorrect", total_questions - correct_count)
        with col4:
            st.metric("Score", f"{percentage:.1f}%")
        
        # Progress Bar
        st.progress(percentage / 100)
        
        # Performance Message
        if percentage >= 80:
            st.success("🎉 Excellent! You've mastered this material!")
        elif percentage >= 60:
            st.info("👍 Good job! Review incorrect topics to improve.")
        else:
            st.warning("📚 Keep studying! Review the lectures and try again.")
        
        # Time Taken
        if st.session_state.timer_enabled and st.session_state.start_time:
            time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
            st.info(f"⏱️ **Time Taken:** {format_time(int(time_taken))}")
        
        # Detailed Results
        with st.expander("📋 View Detailed Results", expanded=True):
            for i, q in enumerate(questions):
                answer_data = st.session_state.answers.get(i, {})
                user_answer = answer_data.get('answer', 'Not answered')
                is_correct = user_answer == q['ans']
                
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**Q{i+1}.** {q['q']}")
                        st.markdown(f"- Your Answer: **{user_answer}**")
                        st.markdown(f"- Correct Answer: **{q['ans']}**")
                        if not is_correct:
                            st.markdown(f"- 💡 {q['exp']}")
                    with col2:
                        if is_correct:
                            st.success("✅")
                        else:
                            st.error("❌")
                    st.markdown("---")
        
        # Export Results
        st.markdown("### 📤 Export Results")
        
        # Create CSV data
        csv_data = "Question ID,Lecture,Question,Your Answer,Correct Answer,Explanation\n"
        for i, q in enumerate(questions):
            answer_data = st.session_state.answers.get(i, {})
            user_answer = answer_data.get('answer', 'Not answered')
            csv_data += f"{q['id']},{q['lec']},\"{q['q']}\",{user_answer},{q['ans']},\"{q['exp']}\"\n"
        
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Again", type="primary", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.show_result = False
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.show_result = False
                st.rerun()
    
    else:
        # Quiz Page
        q = questions[st.session_state.current_question]
        
        # Question Counter & Progress
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f'<p class="question-counter">📍 Question {st.session_state.current_question + 1}/{total_questions}</p>', unsafe_allow_html=True)
        with col2:
            st.progress((st.session_state.current_question + 1) / total_questions)
        with col3:
            is_flagged = st.session_state.current_question in st.session_state.flagged_questions
            if st.button("🚩 Flag" if not is_flagged else "✅ Unflag", key="flag_btn"):
                if is_flagged:
                    st.session_state.flagged_questions.discard(st.session_state.current_question)
                else:
                    st.session_state.flagged_questions.add(st.session_state.current_question)
                st.rerun()
        
        st.markdown("---")
        
        # Question Navigation Grid
        with st.expander("📍 Question Navigator", expanded=False):
            cols_per_row = 10
            total_rows = (total_questions + cols_per_row - 1) // cols_per_row
            
            for row in range(total_rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    q_num = row * cols_per_row + col_idx
                    if q_num < total_questions:
                        with cols[col_idx]:
                            is_answered = q_num in st.session_state.answers
                            is_current = q_num == st.session_state.current_question
                            is_flagged = q_num in st.session_state.flagged_questions
                            
                            button_label = f"{q_num + 1}"
                            if is_flagged:
                                button_label = f"🚩{q_num + 1}"
                            
                            if st.button(button_label, key=f"nav_{q_num}", 
                                       use_container_width=True,
                                       type="primary" if is_current else "secondary"):
                                st.session_state.current_question = q_num
                                st.rerun()
        
        st.markdown("---")
        
        # Question Display
        st.markdown(f"### 📝 Question {st.session_state.current_question + 1}")
        st.markdown(f"**Lecture {q['lec']}**")
        st.markdown(f"**{q['q']}**")
        
        # Get current answer if exists
        current_answer = st.session_state.answers.get(st.session_state.current_question, {}).get('answer')
        
        # FIXED: Display full option text
        options = q['opts']  # Just use the options list directly
        
        # Find the index of the current answer
        current_index = None
        if current_answer:
            for i, opt in enumerate(options):
                if opt.startswith(f"{current_answer})"):
                    current_index = i
                    break
        
        selected_option = st.radio(
            "Select your answer:",
            options,  # ✅ Use full options list
            index=current_index,
            key=f"q_{st.session_state.current_question}"
        )
        
        # Save answer - extract just the letter
        if selected_option:
            selected_letter = selected_option.split(')')[0].strip()
            st.session_state.answers[st.session_state.current_question] = {
                'answer': selected_letter,
                'question': q['q'],
                'correct_answer': q['ans']
            }
        
        st.markdown("---")
        
        # Navigation Buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_question == 0, use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            if st.button("➡️ Next", disabled=st.session_state.current_question >= total_questions - 1, use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        
        with col3:
            if st.button("💾 Save & Continue", use_container_width=True):
                st.success("Answer saved!")
                if st.session_state.current_question < total_questions - 1:
                    st.session_state.current_question += 1
                    st.rerun()
        
        with col4:
            if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
                st.session_state.show_result = True
                st.rerun()
        
        # Practice Mode Feedback
        if st.session_state.quiz_mode == "practice":
            # Get answer from session state instead of radio button
            answer_data = st.session_state.answers.get(st.session_state.current_question, {})
            selected_letter = answer_data.get('answer')
            
            if selected_letter:
                st.markdown("---")
                is_correct = selected_letter == q['ans']
                if is_correct:
                    st.success(" Correct!")
                else:
                    st.error(f" Incorrect. Correct answer: **{q['ans']}**")
                
                st.info(f" **Explanation:** {q['exp']}")
        
        # Jump to Section
        st.markdown("---")
        st.markdown("### 🎯 Quick Navigation")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⏮️ First Question", use_container_width=True):
                st.session_state.current_question = 0
                st.rerun()
        with col2:
            unanswered = [i for i in range(total_questions) if i not in st.session_state.answers]
            if unanswered and st.button("🔍 Next Unanswered", use_container_width=True):
                for q_num in unanswered:
                    if q_num > st.session_state.current_question:
                        st.session_state.current_question = q_num
                        st.rerun()
        with col3:
            if st.session_state.flagged_questions and st.button("🚩 Next Flagged", use_container_width=True):
                flagged_sorted = sorted(st.session_state.flagged_questions)
                for q_num in flagged_sorted:
                    if q_num > st.session_state.current_question:
                        st.session_state.current_question = q_num
                        st.rerun()
                st.session_state.current_question = flagged_sorted[0]
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit | Deep Learning & Gen AI Course</p>
    <p>© 2026 Quiz Master | All 300 Questions from 6 Lectures</p>
</div>
""", unsafe_allow_html=True)
