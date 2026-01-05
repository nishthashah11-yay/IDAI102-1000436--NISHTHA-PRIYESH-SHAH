import streamlit as st
import pandas as pd
from datetime import datetime
import turtle
import random

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ShopImpact – Conscious Shopping",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# Data setup
# -----------------------------
IMPACT_MULTIPLIER = {
    "Clothing": 1.5,
    "Electronics": 3.0,
    "Groceries": 0.8,
    "Footwear": 2.0,
    "Second-hand": 0.4
}

GREEN_ALTERNATIVES = {
    "Clothing": ["Organic Cotton Brands", "Local Handloom", "Second-hand Stores"],
    "Electronics": ["Energy Star Products", "Refurbished Electronics"],
    "Groceries": ["Local Farmers Market", "Organic Brands"],
    "Footwear": ["Recycled Material Shoes", "Vegan Leather"],
    "Second-hand": ["Thrift Stores", "Community Swap Events"]
}

ECO_TIPS = [
    "Buying second-hand can reduce emissions by up to 80%",
    "Local products usually have a lower carbon footprint",
    "Repairing items extends their life and saves resources",
    "Choosing quality over quantity reduces waste"
]

# Initialize session state
if "purchases" not in st.session_state:
    st.session_state.purchases = []

# -----------------------------
# Turtle graphics function
# -----------------------------
def draw_leaf():
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(5)
    t.color("green")
    t.begin_fill()
    t.circle(60, 60)
    t.left(120)
    t.circle(60, 60)
    t.end_fill()
    t.hideturtle()
    screen.exitonclick()

# -----------------------------
# Header
# -----------------------------
st.markdown(
    "<h1 style='color:green;'>🌱 ShopImpact</h1>"
    "<h4>Track your shopping. Reduce your carbon footprint.</h4>",
    unsafe_allow_html=True
)

# -----------------------------
# Input section
# -----------------------------
st.subheader("🛒 Log a Purchase")

col1, col2, col3 = st.columns(3)

with col1:
    product_type = st.selectbox("Product Type", list(IMPACT_MULTIPLIER.keys()))

with col2:
    brand = st.text_input("Brand Name")

with col3:
    price = st.number_input("Price ($)", min_value=0.0, step=1.0)

if st.button("Add Purchase"):
    impact = price * IMPACT_MULTIPLIER[product_type]
    st.session_state.purchases.append({
        "Date": datetime.now(),
        "Product": product_type,
        "Brand": brand,
        "Price": price,
        "CO2 Impact": impact
    })
    st.success("Purchase added successfully! 🌍")

    if product_type == "Second-hand":
        st.info("Great choice! Low-impact shopping 🌿")
        draw_leaf()

    st.write("💡 Eco Tip:", random.choice(ECO_TIPS))

# -----------------------------
# Dashboard
# -----------------------------
st.subheader("📊 Monthly Impact Dashboard")

if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)
    df["Month"] = df["Date"].dt.to_period("M")

    total_spend = df["Price"].sum()
    total_impact = df["CO2 Impact"].sum()

    colA, colB = st.columns(2)
    colA.metric("Total Spend ($)", round(total_spend, 2))
    colB.metric("Estimated CO₂ Impact", round(total_impact, 2))

    st.dataframe(df[["Date", "Product", "Brand", "Price", "CO2 Impact"]])

    # -----------------------------
    # Badges
    # -----------------------------
    st.subheader("🏅 Eco Badges")

    if total_impact < 200:
        st.success("🌟 Eco Saver Badge Earned!")
    elif total_impact < 400:
        st.info("👍 Conscious Shopper Badge")
    else:
        st.warning("🚨 High Impact – Try Greener Choices")

    # -----------------------------
    # Suggestions
    # -----------------------------
    st.subheader("🌿 Greener Alternatives")

    last_product = df.iloc[-1]["Product"]
    for alt in GREEN_ALTERNATIVES[last_product]:
        st.write("•", alt)

else:
    st.info("No purchases logged yet. Start adding to see your impact!")

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    "<hr><p style='text-align:center;'>Made with 💚 for sustainable living</p>",
    unsafe_allow_html=True
)
