import streamlit as st
from PIL import Image
import time
import os

# ---- PAGE HEADER ----
html = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">Tutorials & Challenges</h2>
</div>"""
st.markdown(html, unsafe_allow_html=True)

# ---- LOAD IMAGES ----
img1 = Image.open("./images/dumbbell.webp")
img2 = Image.open("./images/squats.jpg")
img3 = Image.open("./images/pushups.jpeg")
img4 = Image.open("./images/shoulder.jpeg")

# ---- ACHIEVEMENTS ----
achievements = {
    "Bicep Curls Master": "Complete 50 Bicep Curls",
    "Squats Champion": "Perform 30 Squats in one session",
    "Pushups Pro": "Achieve 20 Pushups without stopping",
    "Shoulder Press Expert": "Master 15 Shoulder Press reps"
}

# ---- USER SESSION ----
if "progress" not in st.session_state:
    st.session_state.progress = {"Bicep Curls": 0, "Squats": 0, "Pushups": 0, "Shoulder Press": 0}

if "achievements" not in st.session_state:
    st.session_state.achievements = []

# ---- APP MODE SELECTION ----
app_mode = st.sidebar.selectbox(
    "Choose the Tutorial", ["About", "Bicep Curls", "Squats", "Pushups", "Shoulder Press", "Challenges"]
)

# ---- EXERCISE BENEFITS & TIMER FUNCTION ----
def display_timer():
    minutes = st.number_input("Set Timer (Minutes):", min_value=1, max_value=30, value=1)
    if st.button("Start Timer"):
        for i in range(minutes * 60, -1, -1):
            mins, secs = divmod(i, 60)
            st.write(f"Time Remaining: {mins:02}:{secs:02}")
            time.sleep(1)
        st.success("Time's up! Great job!")

def exercise_benefits(benefits):
    st.markdown("### Exercise Benefits")
    st.write("\n".join([f"- {benefit}" for benefit in benefits]))

# ---- ABOUT SECTION ----
if app_mode == "About":
    st.write("---")
    st.header("Explore Video Tutorials")
    st.write("##")
    tutorials = [
        {"title": "Bicep Curls", "image": img1, "link": "https://youtu.be/ykJmrZ5v0Oo"},
        {"title": "Squats", "image": img2, "link": "https://youtu.be/YaXPRqUwItQ"},
        {"title": "Pushups", "image": img3, "link": "https://youtu.be/IODxDxX7oi4"},
        {"title": "Shoulder Press", "image": img4, "link": "https://youtu.be/qEwKCR5JCog"},
    ]
    for tutorial in tutorials:
        with st.container():
            image_column, text_column = st.columns((1, 2))
            with image_column:
                st.image(tutorial["image"], use_container_width=True)  # Updated parameter
            with text_column:
                st.subheader(tutorial["title"])
                st.write(f"Watch this tutorial to learn {tutorial['title']}!")
                st.markdown(f"[Watch Video...]({tutorial['link']})")

# ---- INDIVIDUAL EXERCISE SECTIONS ----
else:
    exercise_info = {
        "Bicep Curls": {
            "image": "./gif/bicep.gif",
            "steps": [
                "Stand with a dumbbell in each hand, arms fully extended downward.",
                "Keep your elbows close to your torso.",
                "Exhale and curl the weights upward, contracting your biceps.",
                "Pause briefly at the top, then slowly lower the weights back.",
                "Repeat for your desired number of reps."
            ],
            "benefits": ["Strengthens your arms", "Improves grip strength", "Enhances forearm muscles"],
            "pdf": "./pdfs/bicep_curls.pdf"
        },
        "Squats": {
            "image": "./gif/squats.gif",
            "steps": [
                "Stand with feet shoulder-width apart.",
                "Push your hips back as you bend your knees.",
                "Lower yourself until your thighs are parallel to the floor.",
                "Keep your chest upright and back straight.",
                "Push through your heels to return to the starting position."
            ],
            "benefits": ["Strengthens legs and glutes", "Improves mobility and balance", "Enhances core stability"],
            "pdf": "./pdfs/squats.pdf"
        },
        "Pushups": {
            "image": "./gif/pushups.gif",
            "steps": [
                "Start in a high plank position.",
                "Lower your body until your chest is just above the floor.",
                "Keep your elbows close to your body.",
                "Push yourself back up to the starting position.",
                "Repeat for your desired number of reps."
            ],
            "benefits": ["Strengthens chest and triceps", "Improves shoulder stability", "Enhances core strength"],
            "pdf": "./pdfs/pushups.pdf"
        },
        "Shoulder Press": {
            "image": "./gif/shoulder.gif",
            "steps": [
                "Hold a dumbbell in each hand, raise them to shoulder height.",
                "Press the dumbbells overhead until your arms are fully extended.",
                "Slowly lower the dumbbells back to the starting position.",
                "Repeat for your desired number of reps."
            ],
            "benefits": ["Strengthens shoulder muscles", "Improves overhead stability", "Enhances upper body strength"],
            "pdf": "./pdfs/shoulder_press.pdf"
        }
    }

    if app_mode in exercise_info:
        exercise = exercise_info[app_mode]
        st.markdown(f"## {app_mode}")
        st.image(exercise["image"], caption=f"{app_mode} Demonstration", use_container_width=True)  # Updated parameter
        st.markdown(f"### Here's a step-by-step guide for {app_mode}:")
        st.write("\n".join([f"{i+1}. {step}" for i, step in enumerate(exercise["steps"])]))
        exercise_benefits(exercise["benefits"])
        st.markdown(f"[Download PDF Guide]({exercise['pdf']})")
        display_timer()

        # Add Progress Tracker
        reps = st.number_input("Enter number of reps completed:", min_value=1, value=1, step=1)
        if st.button("Update Progress"):
            st.session_state.progress[app_mode] += reps
            st.success(f"Updated! Total {app_mode} Reps: {st.session_state.progress[app_mode]}")

# ---- CHALLENGES & GAMIFICATION ----
if app_mode == "Challenges":
    st.markdown("## Fitness Challenges 🎯")
    st.write("Complete these challenges to unlock achievements!")
    for title, desc in achievements.items():
        if title not in st.session_state.achievements:
            st.markdown(f"**{title}**: {desc}")
        else:
            st.success(f"✅ Achievement Unlocked: {title}")

    # Check for Achievement Unlock
    for ex, reps in st.session_state.progress.items():
        if ex == "Bicep Curls" and reps >= 50:
            st.session_state.achievements.append("Bicep Curls Master")
        elif ex == "Squats" and reps >= 30:
            st.session_state.achievements.append("Squats Champion")
        elif ex == "Pushups" and reps >= 20:
            st.session_state.achievements.append("Pushups Pro")
        elif ex == "Shoulder Press" and reps >= 15:
            st.session_state.achievements.append("Shoulder Press Expert")
