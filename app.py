import streamlit as st
from datetime import datetime
import random
import pandas as pd
from PIL import Image, ImageDraw
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🌍 ShopImpact", layout="wide")

theme = st.sidebar.toggle("🌙 Dark Mode")

if theme:
    st.markdown("<style>body{background-color:#121212;color:white}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body{background-color:#e8f5e9}</style>", unsafe_allow_html=True)

st.title("🌍 ShopImpact – Your Eco Shopping Companion")
st.write("Turn everyday shopping into a fun, green mission 🌱")

# ---------------- SESSION STATE ----------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "goal" not in st.session_state:
    st.session_state.goal = 1000

# ---------------- DATA ----------------
IMPACT_MULTIPLIER = {
    "Electronics": 0.6,
    "Clothes": 0.3,
    "Groceries": 0.1,
    "Footwear": 0.4,
    "Second-hand": 0.05
}

ALTERNATIVES = {
    "Electronics": ["Refurbished phones", "Energy-efficient brands"],
    "Clothes": ["Organic cotton", "Second-hand fashion"],
    "Groceries": ["Local produce", "Minimal packaging"],
    "Footwear": ["Vegan leather", "Recycled materials"],
    "Second-hand": ["Reuse stores", "Community swaps"]
}

ECO_TIPS = [
    "🌿 Buying second-hand can cut emissions by 80%.",
    "🚲 Walking & cycling reduce your carbon footprint.",
    "🛠 Repair before you replace!",
    "📦 Choose products with less packaging."
]

QUOTES = [
    "There is no Planet B.",
    "Small steps make a big green difference.",
    "Sustainability is a lifestyle, not a trend."
]

GREEN_REDUCTION_FACTOR = 0.35

# ---------------- ECO BADGE (PIL) ----------------
def draw_leaf():
    img = Image.new("RGBA", (300, 300), (232, 245, 233, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse((80, 40, 220, 200), fill=(76, 175, 80, 255))
    draw.ellipse((100, 80, 200, 260), fill=(56, 142, 60, 255))
    draw.line((150, 200, 150, 280), fill=(121, 85, 72, 255), width=6)
    img.save("leaf.png")

def show_badge():
    if not os.path.exists("leaf.png"):
        draw_leaf()
    st.image("leaf.png", caption="🌱 Eco Badge Unlocked!", width=200)

# ---------------- FUNCTIONS ----------------
def calculate_impact(product, price):
    return price * IMPACT_MULTIPLIER.get(product, 0.2)

def eco_score(total):
    return max(0, min(100, round(100 - total / 20)))

def assign_badge(total):
    if total < 500:
        return "🌱 Eco Saver"
    elif total < 1500:
        return "♻️ Conscious Shopper"
    else:
        return "🌍 Climate Hero"

def achievement_system():
    count = len(st.session_state.purchases)
    if count >= 10:
        return "🏆 10 Purchases Logged!"
    if st.session_state.streak >= 5:
        return "🔥 5-Day Green Streak!"
    return "🎯 Keep Going!"

# ---------------- INPUT ----------------
st.subheader("🛒 Log Your Purchase")

with st.form("purchase_form"):
    product = st.selectbox("Product Type", list(IMPACT_MULTIPLIER.keys()))
    brand = st.text_input("Brand")
    price = st.number_input("Price (₹)", min_value=1)
    submit = st.form_submit_button("Add Purchase")

if submit:
    impact = calculate_impact(product, price)
    st.session_state.purchases.append({
        "product": product,
        "brand": brand,
        "price": price,
        "impact": impact,
        "date": datetime.now()
    })

    if product == "Second-hand":
        st.session_state.streak += 1
        st.success("🌱 Great choice! You went eco-friendly!")
        show_badge()
    else:
        st.session_state.streak = max(0, st.session_state.streak - 1)

    st.info(random.choice(ECO_TIPS))
    st.write("💬", random.choice(QUOTES))

# ---------------- DASHBOARD ----------------
st.subheader("📊 Impact Dashboard")

df = pd.DataFrame(st.session_state.purchases)

total_spend = df["price"].sum() if not df.empty else 0
total_impact = df["impact"].sum() if not df.empty else 0
eco = eco_score(total_impact)

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Spend", f"₹{total_spend}")
c2.metric("🌫 CO₂ Impact", f"{total_impact:.2f}")
c3.metric("🎯 Eco Score", f"{eco}/100")

st.progress(eco)

# ---------------- GOAL TRACKER ----------------
st.subheader("🎯 Monthly Eco Goal")
st.session_state.goal = st.slider("Set your max CO₂ goal", 100, 5000, st.session_state.goal)
st.metric("Remaining", max(0, st.session_state.goal - total_impact))

# ---------------- CHARTS ----------------
if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    st.subheader("📈 Impact Over Time")
    st.line_chart(df.set_index("date")["impact"])

# ---------------- GREEN SIMULATION ----------------
st.subheader("🌍 Green Future Simulator")

adoption = st.slider("Shift purchases to green alternatives (%)", 0, 100, 40)
green_impact = total_impact - (total_impact * (adoption/100) * GREEN_REDUCTION_FACTOR)

sim_df = pd.DataFrame({
    "Scenario": ["Now", "Green Future"],
    "CO₂ Impact": [total_impact, green_impact]
})
st.bar_chart(sim_df.set_index("Scenario"))

st.success(f"🌿 You could reduce {total_impact - green_impact:.2f} CO₂ units!")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🏅 Status")
    st.write(assign_badge(total_impact))
    st.write(achievement_system())

    st.header("🔥 Eco Streak")
    st.metric("Days", st.session_state.streak)

    st.header("📥 Export Data")
    if not df.empty:
        st.download_button("Download CSV", df.to_csv(index=False), "eco_history.csv")

    st.header("🌿 Greener Alternatives")
    for k, v in ALTERNATIVES.items():
        st.markdown(f"**{k}**")
        for item in v:
            st.write("•", item)

# ---------------- HISTORY ----------------
if not df.empty:
    st.subheader("📋 Purchase History")
    st.dataframe(df)

st.caption("🌱 ShopImpact – Smart, Visual & Gamified Sustainability Platform")
