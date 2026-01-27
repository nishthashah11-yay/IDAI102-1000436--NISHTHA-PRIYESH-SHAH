import streamlit as st
from datetime import datetime
import random
import pandas as pd
import turtle
from PIL import Image
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🌍 ShopImpact", layout="wide")

st.markdown("""
<style>
body { background-color: #e8f5e9; }
h1 { color: #2e7d32; }
h2, h3 { color: #1b5e20; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 ShopImpact – Your Eco Shopping Companion")
st.write("Turn everyday shopping into a fun, green mission 🌱")

# ---------------- SESSION STATE ----------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "streak" not in st.session_state:
    st.session_state.streak = 0

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

# ---------------- TURTLE DRAWING ----------------
def draw_leaf():
    t = turtle.Turtle()
    screen = turtle.Screen()
    screen.bgcolor("#e8f5e9")
    t.color("green")
    t.speed(0)

    t.begin_fill()
    t.circle(100, 60)
    t.left(120)
    t.circle(100, 60)
    t.end_fill()

    t.penup()
    t.goto(0, -120)
    t.pendown()
    t.color("brown")
    t.setheading(-90)
    t.forward(80)

    canvas = screen.getcanvas()
    canvas.postscript(file="leaf.ps")
    turtle.bye()

    img = Image.open("leaf.ps")
    img.save("leaf.png")

def show_turtle():
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
        return "⚠️ High Impact User"

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
        show_turtle()
    else:
        st.session_state.streak = max(0, st.session_state.streak - 1)

    st.info(random.choice(ECO_TIPS))
    st.write("💬", random.choice(QUOTES))

# ---------------- DASHBOARD ----------------
st.subheader("📊 Monthly Dashboard")

total_spend = sum(p["price"] for p in st.session_state.purchases)
total_impact = sum(p["impact"] for p in st.session_state.purchases)
eco = eco_score(total_impact)

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Spend", f"₹{total_spend}")
c2.metric("🌫 CO₂ Impact", f"{total_impact:.2f}")
c3.metric("🎯 Eco Score", f"{eco}/100")

st.progress(eco)

# ---------------- GREEN SIMULATION ----------------
st.subheader("🌍 Green Future Simulator")

adoption = st.slider("Shift purchases to green alternatives (%)", 0, 100, 40)
green_impact = total_impact - (total_impact * (adoption/100) * GREEN_REDUCTION_FACTOR)

df = pd.DataFrame({
    "Scenario": ["Now", "Green Future"],
    "CO₂ Impact": [total_impact, green_impact]
})
st.bar_chart(df.set_index("Scenario"))

st.success(f"🌿 You could reduce {total_impact - green_impact:.2f} CO₂ units!")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🏅 Badge")
    st.write(assign_badge(total_impact))

    st.header("🔥 Eco Streak")
    st.metric("Days", st.session_state.streak)

    st.header("🌿 Greener Alternatives")
    for k, v in ALTERNATIVES.items():
        st.markdown(f"**{k}**")
        for item in v:
            st.write("•", item)

# ---------------- HISTORY ----------------
if st.session_state.purchases:
    st.subheader("📋 Purchase History")
    df = pd.DataFrame(st.session_state.purchases)
    st.dataframe(df)

st.caption("🌱 ShopImpact – Making Sustainability Fun & Visual with Python + Streamlit + Turtle")
