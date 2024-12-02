import openai
import toml
import streamlit as st
import os

# ---- CONFIGURE PAGE ----
st.set_page_config(page_title="FIT-BOT Assistant", page_icon="🤖", layout="wide")

# ---- Load secrets.toml configuration ----
secrets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "secrets.toml"))

if os.path.exists(secrets_path):
    with open(secrets_path, "r") as f:
        config = toml.load(f)
else:
    st.error(f"Configuration file `secrets.toml` not found at {secrets_path}. Please provide it.")
    st.stop()

# ---- Set OpenAI API Key ----
openai.api_key = config.get("openai", {}).get("api_key")
if not openai.api_key:
    st.error("OpenAI API key not found in the configuration file. Please check secrets.toml.")
    st.stop()

# ---- Base prompt for the chatbot ----
BASE_PROMPT = [
    {"role": "system", "content": """
You are Prius, an automated Gym assistant to provide workout routines for users and give suggestions.
You first greet the customer, then ask them what type of workout routine they want.
Provide a few workout options and wait for them to finalize. If they ask for changes, make those changes accordingly.
Finally, summarize the plan and confirm if the user wants to add anything else.
Make sure to clarify all questions about exercises and form.
You respond in a short, conversational, and friendly style.
"""}
]

# ---- Initialize session state ----
if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

if "quick_replies" not in st.session_state:
    st.session_state["quick_replies"] = [
        "Suggest a Full-Body Workout",
        "What are some good chest exercises?",
        "Give me a beginner workout routine.",
        "How do I improve my flexibility?",
        "Suggest a HIIT routine."
    ]

# ---- Function to display conversation history dynamically ----
def show_messages():
    for msg in st.session_state["messages"][1:]:
        if msg["role"] == "user":
            st.markdown(f"**🧑‍💻 USER:** {msg['content']}")
        else:
            st.markdown(f"**🤖 BOT:** {msg['content']}")
    st.markdown("---")

# ---- Function to handle user input ----
def handle_input():
    user_message = st.session_state.user_input.strip()
    if not user_message:
        return

    # Add user message to conversation history
    st.session_state["messages"].append({"role": "user", "content": user_message})

    # Generate AI response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to your desired model, e.g., "gpt-4"
            messages=st.session_state["messages"]
        )
        bot_message = response["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": bot_message})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    # Clear user input field
    st.session_state.user_input = ""

# ---- Function to handle quick replies ----
def handle_quick_reply(reply):
    st.session_state["user_input"] = reply
    handle_input()

# ---- Streamlit app layout ----
st.title("FIT-BOT - Your AI Gym Assistant 🤖")
st.markdown("**Ask me anything about fitness, workouts, or health tips!**")
st.markdown("---")

# ---- Display conversation history ----
show_messages()

# ---- Input Section ----
st.text_input("Your message:", key="user_input", on_change=handle_input, placeholder="Type your message here...")

# ---- Quick Replies ----
st.write("**Quick Suggestions:**")
cols = st.columns(5)
for i, reply in enumerate(st.session_state["quick_replies"]):
    with cols[i % 5]:
        if st.button(reply, key=f"quick_reply_{i}"):
            handle_quick_reply(reply)

# ---- Feedback Section ----
st.markdown("---")
st.write("**Was this helpful?**")
cols_feedback = st.columns(2)
with cols_feedback[0]:
    if st.button("👍 Yes"):
        st.success("Thanks for your feedback!")
with cols_feedback[1]:
    if st.button("👎 No"):
        st.warning("Sorry to hear that. We'll improve!")

# ---- Reset Conversation ----
if st.button("Reset Conversation"):
    st.session_state["messages"] = BASE_PROMPT
    st.session_state.user_input = ""
    st.info("Conversation has been reset.")
