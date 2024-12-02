import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Smart Nutrition Tracker", page_icon="🥗", layout="wide")

# ---- LOAD DATA ----
df = pd.read_csv("./food.csv", encoding='mac_roman')

# Check for required columns
required_columns = ["Food", "Serving", "Calories"]
if not all(col in df.columns for col in required_columns):
    st.error("Dataset must include 'Food', 'Serving', and 'Calories' columns.")
    st.stop()

# ---- PAGE TITLE ----
st.title("Smart Nutrition Tracker 🥗")
st.markdown("### Your companion for personalized nutrition insights.")

# ---- USER INPUTS ----
num_dishes = st.number_input("Enter Number of Dishes 🍽️", min_value=1, max_value=10, value=1, step=1)

# ---- TRACKING VARIABLES ----
total_calories = 0
selected_foods = []
calorie_breakdown = []
nutrient_summary = {"Protein": 0, "Carbs": 0, "Fat": 0}

# ---- FOOD TRACKER ----
st.write("## Add Your Meals")
for i in range(int(num_dishes)):
    st.write(f"### Dish {i + 1}")
    food_selected = st.selectbox(
        f"Select Food Item for Dish {i + 1}",
        df['Food'].unique(),
        key=f"food_{i}"
    )
    
    if food_selected:
        servings = st.number_input(
            f"Number of Servings for {food_selected}",
            min_value=1, max_value=10, value=1, step=1, key=f"servings_{i}"
        )
        
        # Fetch data for the selected food
        food_data = df[df["Food"] == food_selected].iloc[0]
        calories = food_data["Calories"] * servings
        
        # Update tracking variables
        total_calories += calories
        selected_foods.append(food_selected)
        calorie_breakdown.append(calories)

        # Optional nutrient breakdown (mock data for uniqueness)
        nutrient_summary["Protein"] += servings * 5  # Example: Assume 5g protein per serving
        nutrient_summary["Carbs"] += servings * 10  # Example: Assume 10g carbs per serving
        nutrient_summary["Fat"] += servings * 2  # Example: Assume 2g fat per serving

        # Display food details
        st.write(f"**Food Item:** {food_selected}")
        st.write(f"**Calories per Serving:** {food_data['Calories']} kcal")
        st.write(f"**Total Calories for {servings} Serving(s):** {calories} kcal")

# ---- SUMMARY ----
st.write("## Summary")
st.metric("Total Calories Consumed", f"{total_calories} kcal")
st.write(f"**Total Protein:** {nutrient_summary['Protein']} g")
st.write(f"**Total Carbs:** {nutrient_summary['Carbs']} g")
st.write(f"**Total Fat:** {nutrient_summary['Fat']} g")

# ---- VISUALIZATIONS ----
if selected_foods:
    # Pie Chart: Calorie Breakdown
    st.write("### Calorie Breakdown")
    pie_chart = px.pie(
        names=selected_foods,
        values=calorie_breakdown,
        title="Calorie Distribution by Food Item",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart)

    # Nutrient Breakdown
    st.write("### Nutrient Breakdown")
    nutrients_chart = go.Figure(data=[
        go.Bar(name="Protein", x=["Protein"], y=[nutrient_summary["Protein"]]),
        go.Bar(name="Carbs", x=["Carbs"], y=[nutrient_summary["Carbs"]]),
        go.Bar(name="Fat", x=["Fat"], y=[nutrient_summary["Fat"]]),
    ])
    nutrients_chart.update_layout(barmode='group', title="Nutrient Breakdown")
    st.plotly_chart(nutrients_chart)

# ---- SET CALORIE GOAL ----
st.write("## Daily Calorie Goal Tracker 🎯")
calorie_goal = st.number_input("Set Your Daily Calorie Goal (kcal):", min_value=500, max_value=5000, value=2000)
if total_calories > calorie_goal:
    st.warning(f"You've exceeded your calorie goal by {total_calories - calorie_goal} kcal.")
else:
    st.success(f"You're within your calorie goal! {calorie_goal - total_calories} kcal remaining.")

# ---- ADDITIONAL FEATURES ----
st.write("## Additional Features")
# Save Meal Plan
if st.button("Save Your Meal Plan"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"meal_plan_{timestamp}.csv"
    meal_plan_df = pd.DataFrame({"Food": selected_foods, "Calories": calorie_breakdown})
    meal_plan_df.to_csv(filename, index=False)
    st.success(f"Meal plan saved as {filename}.")

# Recommendations
st.write("### Personalized Recommendations")
if total_calories > calorie_goal:
    st.info("Consider swapping high-calorie items for lower-calorie alternatives.")
else:
    st.info("Great job! Keep up the good work with balanced meals.")

# ---- FOOTER ----
st.markdown("""
---
#### Smart Nutrition Tracker © 2024
*Track your meals, meet your goals, and live healthier.*
""")
