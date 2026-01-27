import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EcoImpact Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- WHITE MODE CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: white;
    color: black;
}
h1, h2, h3, h4, h5, h6, p, span, label {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []

if "total_impact" not in st.session_state:
    st.session_state.total_impact = 0.0

if "eco_score" not in st.session_state:
    st.session_state.eco_score = 0

if "frame" not in st.session_state:
    st.session_state.frame = 0

# ---------------- CONSTANTS ----------------
IMPACT_MULTIPLIER = {
    "Electronics": 0.7,
    "Fashion": 0.5,
    "Food": 0.3,
    "Home Goods": 0.4,
    "Second-hand": 0.1,
    "Eco-Friendly": 0.05
}

ECO_TIPS = [
    "Carry reusable bags",
    "Avoid plastic bottles",
    "Buy second-hand",
    "Choose local products",
    "Repair instead of replace"
]

# ---------------- TURTLE GRAPHICS ----------------
def turtle_animation(progress, frame):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Track
    ax.plot([0, 100], [5, 5], linewidth=8, color="#C8E6C9")

    # Turtle movement
    x = min(progress, frame % 101)

    # Shell
    shell = plt.Circle((x, 5), 2.2, color="#4CAF50")
    ax.add_patch(shell)

    # Head
    head = plt.Circle((x + 2.5, 5), 1, color="#66BB6A")
    ax.add_patch(head)

    # Legs
    ax.plot([x - 1, x - 2], [4, 3], color="#2E7D32", linewidth=3)
    ax.plot([x - 1, x - 2], [6, 7], color="#2E7D32", linewidth=3)

    ax.text(50, 8, f"Eco Progress: {progress}%", ha="center", fontsize=12)

    st.pyplot(fig)
    plt.close(fig)

# ---------------- TITLE ----------------
st.title("🌱 EcoImpact Pro")
st.markdown("Track your shopping impact with animated eco visuals 🐢")

# ---------------- PURCHASE FORM ----------------
with st.form("purchase_form"):
    category = st.selectbox("Category", list(IMPACT_MULTIPLIER.keys()))
    brand = st.text_input("Brand / Store")
    price = st.number_input("Price (₹)", min_value=1, value=100)

    eco = st.checkbox("Eco-Friendly Purchase 🌱")
    submit = st.form_submit_button("Add Purchase")

if submit:
    impact = price * IMPACT_MULTIPLIER[category] * (0.5 if eco else 1)

    st.session_state.purchases.append({
        "Category": category,
        "Brand": brand,
        "Price": price,
        "Impact": round(impact, 2),
        "Type": "Eco" if eco else "Regular"
    })

    st.session_state.total_impact += impact

# ---------------- DASHBOARD ----------------
if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)

    total_spent = df["Price"].sum()
    eco_score = int(max(0, 100 - (st.session_state.total_impact / total_spent * 100)))
    st.session_state.eco_score = eco_score

    col1, col2 = st.columns(2)
    col1.metric("Total Spent", f"₹{int(total_spent)}")
    col2.metric("Eco Score", f"{eco_score}/100")

    # Animate turtle
    st.session_state.frame += 3
    turtle_animation(eco_score, st.session_state.frame)

    st.markdown("### Purchase History")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Log your first purchase to see the turtle move 🐢")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("### Eco Tip")
st.sidebar.success(ECO_TIPS[st.session_state.eco_score % len(ECO_TIPS)])

if st.sidebar.button("Reset Data"):
    st.session_state.clear()
    st.rerun()
