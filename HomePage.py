import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image

# ---- CONFIGURE PAGE ----
st.set_page_config(page_title="FitSphere AI", page_icon="💪", layout="wide")

# ---- FUNCTION TO LOAD LOTTIE FILES ----
def load_lottieurl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# ---- FUNCTION TO APPLY LOCAL CSS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("./styles/styles.css")  # Path to the CSS file

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_FYx0Ph.json")
music = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ikk4jhps.json")
podcast = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_JjpNLdaKYX.json")
hero_animation = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_tutdw4n3.json")  # Updated working URL
logo_path = "./images/logo.png"  # Path to the logo file

# ---- HEADER SECTION ----
with st.container():
    # Display Logo
    logo_col, title_col = st.columns([1, 4])
    with logo_col:
        st.image(logo_path, width=100)  # Adjust width to fit
    with title_col:
        st.markdown(
            """
            <div style="background-color: #BB86FC; padding: 10px; border-radius: 8px;">
                <h1 style="color: white; text-align: center; font-size: 36px;">FitSphere AI</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write("**Welcome to FitSphere AI - Your AI-Powered Fitness Companion**")
    if hero_animation:
        st_lottie(hero_animation, height=250, key="hero")

# ---- ABOUT US ----
with st.container():
    st.write("---")
    st.write("## About Us :point_down:")
    left_column, right_column = st.columns(2)
    with left_column:
        st.write(
            """
            Welcome to FitSphere AI! We are here to revolutionize your fitness journey by providing:
            - Personalized AI-driven fitness plans.
            - The convenience of working out at home with expert guidance.
            - Affordable options that are cheaper than traditional gyms.

            🌟 Join us today and take the first step toward a healthier you!
            """
        )
    with right_column:
        if lottie_coding:
            st_lottie(lottie_coding, height=300, key="coding")

# ---- FEATURED PROJECTS ----
with st.container():
    st.write("---")
    st.header("🎶 Get Fit, Jam On, Repeat!")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        if music:
            st_lottie(music, height=300, key="music")
    with text_column:
        st.subheader("Workout Music")
        st.write("Power up your workout with the ultimate music fuel!")
        st.markdown(
            "[🎧 Listen Now](https://open.spotify.com/playlist/6N0Vl77EzPm13GIOlEkoJn?si=9207b7744d094bd3)"
        )

    image_column, text_column = st.columns((1, 2))
    with image_column:
        if podcast:
            st_lottie(podcast, height=300, key="podcast")
    with text_column:
        st.subheader("Fitness Podcasts")
        st.write("Immerse yourself in motivational podcasts to elevate your fitness experience!")
        st.markdown(
            "[🎙️ Listen Now](https://open.spotify.com/playlist/09Ig7KfohF5WmU9RhbDBjs?si=jyZ79y3wQgezrEDHim0NvQ)"
        )

# ---- TESTIMONIALS ----
with st.container():
    st.write("---")
    st.header("What Our Users Say 💬")
    st.write("##")
    testimonials = [
        {"name": "Rahgul", "feedback": "FitSphere AI has transformed my fitness routine!"},
        {"name": "Gukan", "feedback": "I love the AI-driven plans, so convenient and effective!"},
        {"name": "priti", "feedback": "Great platform for home workouts! Highly recommend."},
    ]
    for testimonial in testimonials:
        st.markdown(f"**{testimonial['name']}**")
        st.write(f"\"{testimonial['feedback']}\"")
        st.write("---")

# ---- FAQ SECTION ----
with st.container():
    st.write("---")
    st.header("Frequently Asked Questions 🤔")
    st.write("##")
    st.markdown("### Q: How does FitSphere AI work?")
    st.write("A: FitSphere AI uses AI-driven algorithms to provide personalized fitness plans tailored to your needs.")
    st.markdown("### Q: Is it free to use?")
    st.write("A: Yes, our basic features are free. Premium features are available at an affordable subscription.")
    st.markdown("### Q: Can I cancel anytime?")
    st.write("A: Yes, you can cancel your subscription anytime with no hassle.")

# ---- CONTACT FORM ----
with st.container():
    st.write("---")
    st.header("📞 Get in Touch")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/apabishekraj@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_autoresponse" value="Thank you for contacting FitSphere AI! We will get back to you soon.">
        <input type="hidden" name="_next" value="https://yourwebsite.com/thank-you">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Message Here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """

    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

# ---- FOOTER ----
with st.container():
    st.write("---")
    st.markdown(
        """
        <div style="text-align: center; color: grey;">
            © 2024 FitSphere AI. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )
