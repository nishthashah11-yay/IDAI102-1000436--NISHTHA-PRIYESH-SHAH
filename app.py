import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import random
from PIL import Image, ImageDraw
import os

st.set_page_config(page_title="🌍 ShopImpact", layout="wide")

# ---------------- DATA ----------------
IMPACT = {
    "Electronics": 0.6,
    "Clothes": 0.3,
    "Groceries": 0.1,
    "Footwear": 0.4,
    "Second-hand": 0.05
}

XP_RULES = {
    "log": 10,
    "low_impact": 10
}

LEVELS = {
    1: (0, 99),
    2: (100, 249),
    3: (250, 499),
    4: (500, 10000)
}

BADGES = {
    "Eco Saver": "Low total CO₂",
    "Conscious Consumer": "Mostly low-impact items",
    "Sustainability Streaker": "5 eco-friendly days",
    "Green Champion": "CO₂ reduced over time"
}

# ---------------- SESSION ----------------
if "data" not in st.session_state:
    st.session_state.data = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0

# ---------------- FUNCTIONS ----------------
def get_level(xp):
    for lvl, (low, high) in LEVELS.items():
        if low <= xp <= high:
            return lvl
    return 1

def calc_impact(cat, price):
    return price * IMPACT[cat]

def draw_badge():
    img = Image.new("RGBA", (200, 200), (230, 255, 230))
    d = ImageDraw.Draw(img)
    d.ellipse((30, 30, 170, 170), fill=(60, 180, 75))
    d.text((65, 85), "ECO", fill="white")
    img.save("badge.png")

def show_badge():
    if not os.path.exists("badge.png"):
        draw_badge()
    st.image("badge.png", width=120)

# ---------------- UI ----------------
st.title("🌱 ShopImpact – Gamified Conscious Shopping")

with st.form("log"):
    cat = st.selectbox("Product Type", IMPACT.keys())
    brand = st.text_input("Brand")
    price = st.number_input("Price", min_value=1)
    submit = st.form_submit_button("Add Purchase")

if submit:
    impact = calc_impact(cat, price)
    today = datetime.now().date()

    st.session_state.data.append({
        "Category": cat,
        "Brand": brand,
        "Price": price,
        "Impact": impact,
        "Date": today
    })

    st.session_state.xp += XP_RULES["log"]
    if cat == "Second-hand":
        st.session_state.xp += XP_RULES["low_impact"]
        st.session_state.streak += 1
        st.success("🌿 Eco choice! Bonus XP!")
        show_badge()
    else:
        st.session_state.streak = 0

# ---------------- DASHBOARD ----------------
df = pd.DataFrame(st.session_state.data)
total_impact = df["Impact"].sum() if not df.empty else 0
level = get_level(st.session_state.xp)

c1, c2, c3, c4 = st.columns(4)
c1.metric("XP", st.session_state.xp)
c2.metric("Level", level)
c3.metric("Total CO₂", f"{total_impact:.2f}")
c4.metric("Streak", st.session_state.streak)

# ---------------- WEEKLY CHART ----------------
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    weekly = df.groupby(pd.Grouper(key="Date", freq="W"))["Impact"].sum()
    st.subheader("📈 Weekly Impact")
    st.bar_chart(weekly)

# ---------------- BADGES ----------------
st.subheader("🏅 Achievements")

earned = []
if total_impact < 500:
    earned.append("Eco Saver")
if (df["Category"] == "Second-hand").sum() > len(df)/2:
    earned.append("Conscious Consumer")
if st.session_state.streak >= 5:
    earned.append("Sustainability Streaker")
if len(df) > 5 and df["Impact"].iloc[-1] < df["Impact"].iloc[0]:
    earned.append("Green Champion")

for badge in BADGES:
    if badge in earned:
        st.success(f"🏆 {badge}")
    else:
        st.info(f"🔒 {badge}")

# ---------------- HISTORY ----------------
if not df.empty:
    st.subheader("📋 Purchase History")
    st.dataframe(df)

st.caption("Track • Reflect • Improve • Shop Responsibly 🌍")
