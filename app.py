import streamlit as st
import pandas as pd
import time
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🌱 EcoImpact Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- GLOBAL CSS (BLACK TEXT) ----------------
st.markdown("""
<style>
* {
    font-family: 'Poppins', sans-serif;
    color: black !important;
}

h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: black !important;
}

.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "total_impact" not in st.session_state:
    st.session_state.total_impact = 0

if "achievements" not in st.session_state:
    st.session_state.achievements = []

# Use day index instead of datetime
today_index = int(time.time() // 86400)

if "last_login_day" not in st.session_state:
    st.session_state.last_login_day = today_index

if "current_tip" not in st.session_state:
    st.session_state.current_tip = None

# ---------------- CONSTANTS ----------------
IMPACT_MULTIPLIER = {
    "Electronics": 0.7,
    "Fashion": 0.5,
    "Food": 0.3,
    "Home Goods": 0.4,
    "Second-hand": 0.1,
    "Eco-Friendly": 0.05
}

MOTIVATIONAL_QUOTES = [
    "Every small choice creates waves of change!",
    "Your purchases plant seeds for tomorrow's forests",
    "Sustainability isn't a trend—it's a lifestyle revolution",
    "Be the change you wish to see in your shopping cart",
    "Your eco-journey inspires others to follow",
]

ECO_TIPS = [
    "Always carry reusable shopping bags",
    "Use a refillable water bottle instead of plastic",
    "Buy local to reduce transportation emissions",
    "Switch to LED bulbs at home",
    "Repair items instead of replacing",
]

ACHIEVEMENTS = [
    "First Green Purchase",
    "3-Day Eco Streak",
    "5 Eco Purchases",
    "Planet Protector",
    "Earth Guardian"
]

# ---------------- UTIL FUNCTIONS ----------------
def now_string():
    return time.strftime("%Y-%m-%d %H:%M")

def choose(arr):
    return arr[np.random.randint(0, len(arr))]

# ---------------- TURTLE GRAPHICS ----------------
def generate_turtle_animation(score):
    img = Image.new('RGB', (300, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    center = 150
    draw.ellipse([50, 50, 250, 250], fill=(100, 180, 100))

    draw.text((150, 150), f"ECO\n{score}/100",
              fill="black",
              anchor="mm",
              font=ImageFont.load_default())

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def create_turtle_progress(progress):
    progress = int(progress)
    img = Image.new("RGB", (700, 120), (240, 249, 240))
    draw = ImageDraw.Draw(img)

    draw.rectangle([50, 55, 650, 65], fill=(200, 230, 200))
    draw.rectangle([50, 55, 50 + int(6 * progress), 65], fill=(76, 175, 80))

    draw.text((350, 20), f"Progress: {progress}%", fill="black",
              anchor="mm", font=ImageFont.load_default())

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ---------------- TITLE ----------------
st.title("🌱 EcoImpact Pro")
st.markdown("Track your shopping impact and grow your eco-streak 🌍")

# ---------------- DAILY LOGIC ----------------
if today_index != st.session_state.last_login_day:
    st.session_state.streak += 1
    st.session_state.last_login_day = today_index

if st.session_state.current_tip is None:
    st.session_state.current_tip = choose(ECO_TIPS)

# ---------------- HEADER ----------------
st.markdown(f"💬 **{choose(MOTIVATIONAL_QUOTES)}**")
st.markdown(f"🔥 **Eco Streak:** {st.session_state.streak} days")
st.markdown(f"💡 **Tip:** {st.session_state.current_tip}")
st.markdown("---")

# ---------------- PURCHASE FORM ----------------
with st.form("purchase_form"):
    category = st.selectbox("Category", list(IMPACT_MULTIPLIER.keys()))
    brand = st.text_input("Brand / Store")
    price = st.number_input("Price (₹)", min_value=1, value=100)

    col1, col2 = st.columns(2)
    submit_regular = col1.form_submit_button("🛍️ Regular")
    submit_eco = col2.form_submit_button("🌱 Eco")

if submit_regular or submit_eco:
    if not brand:
        st.warning("Brand required")
    else:
        eco = submit_eco or category in ["Second-hand", "Eco-Friendly"]
        impact = price * IMPACT_MULTIPLIER[category] * (0.5 if eco else 1)

        st.session_state.purchases.append({
            "Date": now_string(),
            "Category": category,
            "Brand": brand,
            "Price": price,
            "Impact": round(impact, 1),
            "Type": "Eco" if eco else "Regular"
        })

        st.session_state.total_impact += impact

        if eco:
            st.session_state.streak += 1
            st.success("🌱 Eco purchase logged!")

# ---------------- DASHBOARD ----------------
if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)

    total_spent = df["Price"].sum()
    eco_score = max(0, 100 - (st.session_state.total_impact / total_spent * 100))

    st.metric("Total Spent", f"₹{int(total_spent)}")
    st.metric("Eco Score", f"{int(eco_score)}/100")

    st.image(create_turtle_progress(eco_score))
    st.image(generate_turtle_animation(int(eco_score)), width=200)

    st.dataframe(df, use_container_width=True)

else:
    st.info("Log your first purchase to begin 🌱")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("### Quick Actions")

if st.sidebar.button("Reset Data"):
    st.session_state.clear()
    st.rerun()

if st.sidebar.button("New Tip"):
    st.session_state.current_tip = choose(ECO_TIPS)
    st.rerun()

st.sidebar.metric("Leaderboard Rank", f"#{np.random.randint(1, 50)}")
st.sidebar.metric("Global CO₂ Saved", f"{np.random.randint(10000, 50000)} kg")
