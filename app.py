import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="ShopImpact – Conscious Shopping Dashboard",
    page_icon="🌱",
    layout="wide"
)

# ------------------------------------
# Data Structures
# ------------------------------------
impact_multiplier = {
    "Clothing": 1.5,
    "Electronics": 3.0,
    "Groceries": 0.8,
    "Footwear": 2.0,
    "Second-hand": 0.4
}

green_alternatives = {
    "Clothing": ["Organic cotton brands", "Local handloom", "Second-hand clothes"],
    "Electronics": ["Energy Star products", "Refurbished electronics"],
    "Groceries": ["Local farmers market", "Organic groceries"],
    "Footwear": ["Shoes made from recycled materials", "Vegan leather footwear"],
    "Second-hand": ["Thrift stores", "Community swap events"]
}

eco_tips = [
    "Buying second-hand reduces carbon emissions significantly.",
    "Local products usually have a smaller carbon footprint.",
    "Repairing items helps reduce waste.",
    "Eco-friendly choices protect future generations."
]

# ------------------------------------
# Session State
# ------------------------------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []

# ------------------------------------
# Eco Reward Visual (Turtle Replacement)
# ------------------------------------
def eco_reward():
    st.success("🌿 Eco-friendly choice!")
    st.markdown(
        "<div style='text-align:center; font-size:60px;'>🌱 🌿 🍃</div>",
        unsafe_allow_html=True
    )

# ------------------------------------
# App Header
# ------------------------------------
st.markdown(
    """
    <h1 style='color:green;'>🌱 ShopImpact</h1>
    <h4>Track your shopping and reduce your environmental impact</h4>
    """,
    unsafe_allow_html=True
)

# ------------------------------------
# Purchase Input Section
# ------------------------------------
st.subheader("🛒 Log a Purchase")

col1, col2, col3 = st.columns(3)

with col1:
    product = st.selectbox("Product Type", list(impact_multiplier.keys()))

with col2:
    brand = st.text_input("Brand Name")

with col3:
    price = st.number_input("Price ($)", min_value=0.0, step=1.0)

if st.button("Add Purchase"):
    co2 = price * impact_multiplier[product]

    st.session_state.purchases.append({
        "Date": datetime.now(),
        "Product": product,
        "Brand": brand,
        "Price": price,
        "CO2 Impact": co2
    })

    st.success("Purchase added successfully!")

    if product == "Second-hand":
        eco_reward()

    st.info(f"💡 Eco Tip: {random.choice(eco_tips)}")

# ------------------------------------
# Dashboard Section
# ------------------------------------
st.subheader("📊 Monthly Impact Dashboard")

if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)

    total_spend = df["Price"].sum()
    total_impact = df["CO2 Impact"].sum()

    colA, colB = st.columns(2)
    colA.metric("💰 Total Spend ($)", round(total_spend, 2))
    colB.metric("🌍 Estimated CO₂ Impact", round(total_impact, 2))

    st.dataframe(df)

    # --------------------------------
    # Badges
    # --------------------------------
    st.subheader("🏅 Eco Badges")

    if total_impact < 200:
        st.success("🌟 Eco Saver Badge Earned!")
    elif total_impact < 400:
        st.info("👍 Conscious Shopper Badge")
    else:
        st.warning("🚨 High Impact – Consider greener choices")

    # --------------------------------
    # Suggestions
    # --------------------------------
    st.subheader("🌿 Greener Alternatives")

    last_product = df.iloc[-1]["Product"]
    for alt in green_alternatives[last_product]:
        st.write("•", alt)

else:
    st.info("No purchases added yet. Start logging to see your impact!")

# ------------------------------------
# Footer
# ------------------------------------
st.markdown(
    "<hr><p style='text-align:center;'>Made with 💚 for sustainable living</p>",
    unsafe_allow_html=True
)
