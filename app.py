import streamlit as st
from datetime import datetime
import random
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ShopImpact – Conscious Shopping Dashboard",
    layout="wide"
)

st.title("🌍 ShopImpact – Conscious Shopping Dashboard")
st.write(
    "ShopImpact helps you understand the environmental impact of your purchases "
    "and explores how adopting greener alternatives can significantly reduce CO₂ emissions."
)

# ---------------- SESSION STATE ----------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

# ---------------- DATA DEFINITIONS ----------------
IMPACT_MULTIPLIER = {
    "Electronics": 0.6,
    "Clothes": 0.3,
    "Groceries": 0.1,
    "Footwear": 0.4,
    "Second-hand": 0.05
}

ALTERNATIVES = {
    "Electronics": ["Refurbished devices", "Energy-efficient brands"],
    "Clothes": ["Organic cotton", "Second-hand clothing"],
    "Groceries": ["Local produce", "Minimal packaging brands"],
    "Footwear": ["Vegan leather", "Sustainable materials"],
    "Second-hand": ["Reuse stores", "Community swaps"]
}

ECO_TIPS = [
    "Buying second-hand can reduce emissions by more than 80%.",
    "Local products minimize transport-related CO₂.",
    "Repairing instead of replacing extends product life.",
    "Minimal packaging significantly reduces waste."
]

QUOTES = [
    "Small daily actions lead to big environmental change.",
    "Sustainability is not a sacrifice, it's a smarter choice.",
    "There is no Planet B."
]

GREEN_REDUCTION_FACTOR = 0.35  # 35% reduction when green alternatives are adopted

# ---------------- FUNCTIONS ----------------
def calculate_impact(product, price):
    return price * IMPACT_MULTIPLIER.get(product, 0.2)

def assign_badge(total_impact):
    if total_impact < 500:
        return "🌱 Eco Saver"
    elif total_impact < 1500:
        return "♻️ Conscious Shopper"
    else:
        return "⚠️ High Impact Month"

def eco_score(total_impact):
    score = 100 - (total_impact / 20)
    return max(0, min(100, round(score)))

def impact_category(total_impact):
    if total_impact < 500:
        return "🟢 Low Impact"
    elif total_impact < 1500:
        return "🟡 Medium Impact"
    else:
        return "🔴 High Impact"

def previous_month_str():
    now = datetime.now()
    if now.month == 1:
        return f"{now.year - 1}-12"
    return f"{now.year}-{now.month - 1:02d}"

def projected_green_impact(current_impact, adoption_rate):
    reduced = current_impact * adoption_rate * GREEN_REDUCTION_FACTOR
    return round(current_impact - reduced, 2)

def category_impact_summary(purchases):
    summary = {}
    for p in purchases:
        summary[p["product"]] = summary.get(p["product"], 0) + p["impact"]
    return summary

# ---------------- INPUT FORM ----------------
st.subheader("🛒 Log a Purchase")

with st.form("purchase_form"):
    product = st.selectbox("Product Category", list(IMPACT_MULTIPLIER.keys()))
    brand = st.text_input("Brand Name (optional)")
    price = st.number_input("Price (₹)", min_value=0)
    submitted = st.form_submit_button("Add Purchase")

if submitted:
    impact = calculate_impact(product, price)
    st.session_state.purchases.append({
        "product": product,
        "brand": brand,
        "price": price,
        "impact": impact,
        "month": datetime.now().strftime("%Y-%m"),
        "date": datetime.now().date()
    })

    if product == "Second-hand":
        st.session_state.streak += 1
    else:
        st.session_state.streak = max(0, st.session_state.streak - 1)

    st.success("✅ Purchase added successfully!")

# ---------------- DASHBOARD METRICS ----------------
st.subheader("📊 Monthly Impact Overview")

current_month = datetime.now().strftime("%Y-%m")
monthly_purchases = [
    p for p in st.session_state.purchases if p["month"] == current_month
]

total_spend = sum(p["price"] for p in monthly_purchases)
total_impact = sum(p["impact"] for p in monthly_purchases)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Spend", f"₹{total_spend}")
col2.metric("🌫️ Estimated CO₂ Impact", f"{total_impact:.2f} units")
eco = eco_score(total_impact)
col3.metric(
    "🎯 Eco Score", f"{eco} / 100", delta=f"{eco}%"
)

# ---------------- TREND INSIGHTS ----------------
prev_month = previous_month_str()
prev_month_impact = sum(
    p["impact"] for p in st.session_state.purchases if p["month"] == prev_month
)

if prev_month_impact > 0:
    delta = total_impact - prev_month_impact
    st.info(
        f"Compared to last month, your CO₂ impact is "
        f"{'lower' if delta < 0 else 'higher'} by {abs(round(delta, 2))} units."
    )

# ---------------- GREEN TRANSITION SIMULATION ----------------
st.subheader("🌱 Green Transition Simulation")
st.write(
    "Compare your **current impact** with a **projected scenario** "
    "if some purchases are shifted to greener alternatives."
)

adoption_percentage = st.slider(
    "Percentage of purchases shifted to green alternatives",
    0, 100, 40, step=10
)
adoption_rate = adoption_percentage / 100
green_impact = projected_green_impact(total_impact, adoption_rate)
reduction = total_impact - green_impact

# Display bar chart
comparison_df = pd.DataFrame({
    "Scenario": ["Current Practices", "After Green Transition"],
    "Estimated CO₂ Impact (units)": [total_impact, green_impact]
})
st.bar_chart(data=comparison_df.set_index("Scenario"))

st.success(
    f"🌍 Projected CO₂ Reduction: **{reduction:.2f} units** "
    f"({adoption_percentage}% green adoption)"
)

# ---------------- GAMIFICATION ----------------
st.subheader("🎮 Green Progress & Rewards")
reduction_percent = (reduction / total_impact * 100) if total_impact > 0 else 0
st.progress(min(int(reduction_percent), 100))

if reduction_percent >= 40:
    st.success("🏆 Green Champion Badge Unlocked!")
elif reduction_percent >= 20:
    st.info("🥈 Eco Improver Badge Earned!")
elif reduction_percent > 0:
    st.warning("🥉 First Green Step Taken!")
else:
    st.write("🌿 Make greener choices to unlock rewards.")

st.metric("🔥 Sustainable Choice Streak", f"{st.session_state.streak} actions")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🏅 Monthly Badge")
    st.write(assign_badge(total_impact))

    st.header("🌿 Suggested Greener Alternatives")
    for category, alternatives in ALTERNATIVES.items():
        st.markdown(f"**{category}:**")
        for alt in alternatives:
            st.write(f"• {alt}")

    st.header("💡 Eco Tip")
    st.info(random.choice(ECO_TIPS))

    st.header("🎯 Eco Score")
    st.metric("Current Score", f"{eco} / 100", delta=f"{eco}%")

    st.header("🔥 Streak")
    st.metric("Actions Streak", f"{st.session_state.streak}")

# ---------------- PURCHASE HISTORY ----------------
if st.session_state.purchases:
    st.subheader("📋 Purchase History")
    df = pd.DataFrame(st.session_state.purchases)
    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)

# ---------------- FOOTER ----------------
st.write("---")
st.caption(
    "Disclaimer: CO₂ values are estimates for educational purposes. "
    "The green transition scenario represents a modeled projection, not real-world measurements."
)
