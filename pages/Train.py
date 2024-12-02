import streamlit as st
import cv2
from cvzone.PoseModule import PoseDetector
import math
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import time
import os

# ---- Initialize Session State Variables ----
if "exercise_type" not in st.session_state:
    st.session_state.exercise_type = None
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "direction" not in st.session_state:
    st.session_state.direction = 0
if "workout_history" not in st.session_state:
    st.session_state.workout_history = []

# ---- Angle Finder Class ----
class AngleFinder:
    def __init__(self, lmlist, p1, p2, p3):
        self.lmlist = lmlist
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def calculate_angle(self):
        if len(self.lmlist) != 0:
            try:
                x1, y1 = self.lmlist[self.p1][1:3]
                x2, y2 = self.lmlist[self.p2][1:3]
                x3, y3 = self.lmlist[self.p3][1:3]
                angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
                return abs(angle)
            except (IndexError, ValueError):
                return None
        return None

# ---- Start Exercise ----
def start_exercise(detector, exercise_name, angle_indices, goal_calories, weight):
    cap = cv2.VideoCapture(0)
    counter = 0
    direction = 0
    start_time = time.time()
    frame_placeholder = st.empty()
    progress_placeholder = st.empty()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (640, 480))
        detector.findPose(img, draw=False)
        lmList, _ = detector.findPosition(img, draw=False)

        angle_finder = AngleFinder(lmList, *angle_indices)
        angle = angle_finder.calculate_angle()

        if angle is not None:
            if angle > 160 and direction == 0:
                counter += 0.5
                direction = 1
            if angle < 100 and direction == 1:
                counter += 0.5
                direction = 0

        # Real-Time Feedback
        feedback = "Good form!" if angle is not None and angle > 160 else "Adjust your posture!"
        cv2.putText(img, feedback, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display Counter
        cv2.putText(img, f"Reps: {int(counter)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(img)

        # Progress Tracker
        calories_burned = counter * weight * 0.1
        progress = min(calories_burned / goal_calories * 100, 100)
        progress_placeholder.progress(int(progress))

        if st.session_state.exercise_type == "Stop" or progress >= 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    duration = time.time() - start_time
    show_analytics(counter, calories_burned, goal_calories, exercise_name, duration)

# ---- Show Analytics ----
def show_analytics(counter, calories_burned, goal_calories, exercise_name, duration):
    st.write(f"### Workout Summary: {exercise_name}")
    st.write(f"**Reps Completed:** {int(counter)}")
    st.write(f"**Calories Burned:** {calories_burned:.2f} kcal")
    st.write(f"**Time Taken:** {int(duration // 60)} min {int(duration % 60)} sec")

    st.session_state.workout_history.append({
        "Exercise": exercise_name,
        "Reps": int(counter),
        "Calories Burned": round(calories_burned, 2),
        "Time Taken (min)": round(duration / 60, 2)
    })

    # Bar Chart
    fig = go.Figure(data=[
        go.Bar(name="Calories Burned", x=[exercise_name], y=[calories_burned]),
        go.Bar(name="Goal Calories", x=[exercise_name], y=[goal_calories])
    ])
    fig.update_layout(title="Calories Burned vs Goal", barmode="group")
    st.plotly_chart(fig)

# ---- Workout History Viewer ----
def show_workout_history():
    if st.session_state.workout_history:
        st.write("### Workout History")
        history_df = pd.DataFrame(st.session_state.workout_history)
        st.dataframe(history_df)

        csv_path = "workout_history.csv"
        history_df.to_csv(csv_path, index=False)
        with open(csv_path, "rb") as file:
            st.download_button(
                label="Download Workout History",
                data=file,
                file_name="workout_history.csv",
                mime="text/csv"
            )
    else:
        st.write("No workout history available. Start your first session!")

# ---- Main Program ----
st.title("Advanced AI Fitness Trainer 🏋️")
exercise = st.sidebar.selectbox(
    "Choose an Exercise",
    ["About", "Squats", "Pushups", "Left Dumbbell", "Right Dumbbell", "Plank", "Jumping Jacks"]
)

if exercise == "About":
    st.header("Welcome to AI Fitness Trainer!")
    st.write("""
        - Choose your workout from the sidebar.
        - Ensure your webcam is set up for proper pose detection.
        - Stay in a well-lit area for accurate tracking.
        - Track your progress and download workout history.
    """)
else:
    weight = st.slider("Enter your weight (kg):", 20, 150, 70)
    goal_calories = st.slider("Set a calorie goal:", 10, 500, 50)

    if st.button("Start"):
        st.session_state.exercise_type = "Start"
    if st.button("Stop"):
        st.session_state.exercise_type = "Stop"

    detector = PoseDetector(detectionCon=0.7, trackCon=0.7)

    if st.session_state.exercise_type == "Start":
        if exercise == "Squats":
            start_exercise(detector, "Squats", [24, 26, 28], goal_calories, weight)
        elif exercise == "Pushups":
            start_exercise(detector, "Pushups", [11, 13, 15], goal_calories, weight)
        elif exercise == "Left Dumbbell":
            start_exercise(detector, "Left Dumbbell", [11, 13, 15], goal_calories, weight)
        elif exercise == "Right Dumbbell":
            start_exercise(detector, "Right Dumbbell", [12, 14, 16], goal_calories, weight)
        elif exercise == "Plank":
            start_exercise(detector, "Plank", [11, 13, 15], goal_calories, weight)
        elif exercise == "Jumping Jacks":
            start_exercise(detector, "Jumping Jacks", [24, 26, 28], goal_calories, weight)

# Display Workout History
show_workout_history()
