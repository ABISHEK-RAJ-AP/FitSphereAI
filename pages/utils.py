import streamlit as st
import time
import os

# ---- CONFIGURE PAGE ----
st.set_page_config(page_title="Utils", page_icon="🛠️", layout="wide")

# ---- HEADER ----
st.markdown(
    """
    <div style="background-color:#BB86FC; padding:10px; border-radius:8px;">
        <h1 style="text-align:center; color:white;">Utilities</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- BMI CALCULATOR ----
st.write("## BMI Calculator 🧮")
weight = st.number_input("Enter your weight (kg):", min_value=1, max_value=300, value=70)
height = st.number_input("Enter your height (cm):", min_value=50, max_value=250, value=170)

if st.button("Calculate BMI"):
    bmi = weight / ((height / 100) ** 2)
    st.write(f"Your BMI is **{bmi:.2f}**.")
    if bmi < 18.5:
        st.write("You're classified as **underweight**. Consider consulting a healthcare provider.")
    elif 18.5 <= bmi < 24.9:
        st.write("You're classified as **normal weight**. Great job!")
    elif 25 <= bmi < 29.9:
        st.write("You're classified as **overweight**. Keep an eye on your health.")
    else:
        st.write("You're classified as **obese**. Consider a fitness plan.")

# ---- CALORIE NEEDS CALCULATOR ----
st.write("## Calorie Needs Calculator 🍎")
st.write("Estimate your daily calorie requirements based on your activity level.")

age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
gender = st.radio("Select your gender:", ["Male", "Female"])
activity_level = st.selectbox(
    "Select your activity level:",
    [
        "Sedentary (little or no exercise)",
        "Lightly active (light exercise/sports 1-3 days/week)",
        "Moderately active (moderate exercise/sports 3-5 days/week)",
        "Very active (hard exercise/sports 6-7 days/week)",
        "Extra active (very hard exercise, physical job, or training)",
    ],
)

if st.button("Calculate Calories"):
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
    activity_multiplier = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days/week)": 1.725,
        "Extra active (very hard exercise, physical job, or training)": 1.9,
    }
    calories = bmr * activity_multiplier[activity_level]
    st.write(f"Your estimated daily calorie requirement is **{calories:.2f} kcal**.")

# ---- WORKOUT TIMER WITH COUNTDOWN ----
st.write("## Workout Timer ⏱️")
st.write("Set a timer for your workouts (e.g., HIIT, yoga, or stretching).")
timer_minutes = st.number_input("Set timer (minutes):", min_value=1, max_value=60, value=5)
if st.button("Start Timer"):
    st.write(f"Countdown Timer for **{timer_minutes} minutes**:")
    countdown_seconds = timer_minutes * 60

    with st.empty():
        for seconds_left in range(countdown_seconds, -1, -1):
            minutes, seconds = divmod(seconds_left, 60)
            st.write(f"Time Remaining: **{minutes:02}:{seconds:02}**")
            time.sleep(1)
    st.success("Time's up! Great job on your workout!")

# ---- WATER INTAKE CALCULATOR ----
st.write("## Daily Water Intake Calculator 💧")
st.write("Calculate how much water you should drink daily based on your weight.")
water_weight = st.number_input("Enter your weight (kg) for water calculation:", min_value=1, max_value=300, value=70)

if st.button("Calculate Water Intake"):
    water_intake = water_weight * 0.033
    st.write(f"Your recommended daily water intake is **{water_intake:.2f} liters**.")

# ---- EXTERNAL RESOURCES ----
st.write("## External Fitness Resources 🌐")
st.markdown(
    """
    - [MyFitnessPal](https://www.myfitnesspal.com/) - Track your meals and workouts.
    - [Nike Training Club](https://www.nike.com/ntc-app) - Free workout app with guided routines.
    - [Yoga with Adriene](https://www.youtube.com/user/yogawithadriene) - Free yoga classes on YouTube.
    """
)

# ---- DOWNLOADABLE WORKOUT PLANS ----
st.write("## Downloadable Workout Plans 📥")
st.markdown(
    """
    Here are some great workout plans you can access directly:
    
    - [Beginner Bodyweight Workout](https://thefitnessphantom.com/wp-content/uploads/2021/05/Beginner-Bodyweight-Workout-Plan.pdf)
    - [Advanced Full Body Workout](https://thefitnessphantom.com/wp-content/uploads/2021/05/Advanced-Full-Body-Workout.pdf)
    - [8 Week Gym Workout Plan](https://thefitnessphantom.com/wp-content/uploads/2021/05/8-Week-Gym-Workout-Plan.pdf)
    
    Click the links above to view or download the PDFs directly from **The Fitness Phantom**.
    """
)
