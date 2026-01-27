import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from PIL import Image, ImageDraw, ImageFont
import io

# Page configuration
st.set_page_config(
    page_title="ShopImpact - Conscious Shopping Dashboard",
    page_icon="🌱",
    layout="wide"
)
# ---------------- CUSTOM STYLES ----------------
st.markdown("""
<style>
/* Main background */
body, .stApp {
    background-color: #e8f5e9;  /* light green */
    color: #1b5e20;             /* dark green text */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #a5d6a7; /* pastel green */
    color: #1b5e20;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #2e7d32;  /* dark green for headers */
}

/* Buttons */
.stButton > button {
    background-color: #66bb6a;  /* green button */
    color: white;
    border-radius: 12px;
    padding: 0.5em 1em;
    font-weight: bold;
}

/* Hover effect for buttons */
.stButton > button:hover {
    background-color: #43a047; /* darker green */
    color: white;
}

/* Slider */
.css-1aumxhk .stSlider > div > div:nth-child(1) {
    background-color: #66bb6a !important;
}

/* Progress bar */
.css-1v3fvcr .stProgress > div > div > div {
    background-color: #43a047 !important;
}

/* Info box */
.stInfo {
    background-color: #c8e6c9 !important;
    color: #1b5e20 !important;
}

/* Success box */
.stSuccess {
    background-color: #81c784 !important;
    color: #1b5e20 !important;
}

/* Error box */
.stError {
    background-color: #ef9a9a !important;
    color: white !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #2e7d32;
    font-weight: bold;
}

/* Dataframe table header */
.css-1d391kg th {
    background-color: #a5d6a7;
    color: #1b5e20;
    font-weight: bold;
}

/* Download button */
.stDownloadButton > button {
    background-color: #66bb6a;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'purchases' not in st.session_state:
    st.session_state.purchases = []
if 'current_xp' not in st.session_state:
    st.session_state.current_xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'eco_streak' not in st.session_state:
    st.session_state.eco_streak = 0
if 'last_purchase_date' not in st.session_state:
    st.session_state.last_purchase_date = None
if 'badges' not in st.session_state:
    st.session_state.badges = []

# CO₂ Impact Multipliers (kg CO₂ per $ spent)
CO2_MULTIPLIERS = {
    "Clothing": 3.5,
    "Electronics": 10.2,
    "Food & Groceries": 1.8,
    "Personal Care": 2.1,
    "Home Goods": 2.8,
    "Transportation": 12.5,
    "Entertainment": 1.2,
    "Books & Education": 0.8,
    "Sports & Outdoors": 1.5,
    "Other": 2.0
}

# XP values based on CO₂ impact
def calculate_xp(co2_impact):
    if co2_impact < 5:
        return 50  # Low impact = high XP
    elif co2_impact < 15:
        return 30  # Medium impact
    else:
        return 10  # High impact

# Level thresholds
LEVEL_THRESHOLDS = {1: 0, 2: 200, 3: 500, 4: 1000}

def update_level():
    xp = st.session_state.current_xp
    if xp >= 1000:
        st.session_state.level = 4
    elif xp >= 500:
        st.session_state.level = 3
    elif xp >= 200:
        st.session_state.level = 2
    else:
        st.session_state.level = 1

# Badge earning logic
def check_badges():
    badges_earned = []
    
    # Calculate total CO₂
    total_co2 = sum(p['co2_impact'] for p in st.session_state.purchases) if st.session_state.purchases else 0
    
    # Badge 1: Eco Saver (total CO₂ < 50)
    if total_co2 < 50 and "Eco Saver" not in st.session_state.badges:
        st.session_state.badges.append("Eco Saver")
        badges_earned.append("Eco Saver")
    
    # Badge 2: Conscious Consumer (>50% low impact purchases)
    if st.session_state.purchases:
        low_impact_count = sum(1 for p in st.session_state.purchases if p['co2_impact'] < 5)
        if low_impact_count / len(st.session_state.purchases) > 0.5 and "Conscious Consumer" not in st.session_state.badges:
            st.session_state.badges.append("Conscious Consumer")
            badges_earned.append("Conscious Consumer")
    
    # Badge 3: Sustainability Streaker (5-day streak)
    if st.session_state.eco_streak >= 5 and "Sustainability Streaker" not in st.session_state.badges:
        st.session_state.badges.append("Sustainability Streaker")
        badges_earned.append("Sustainability Streaker")
    
    # Badge 4: Green Champion (reduced impact over time)
    if len(st.session_state.purchases) >= 10:
        recent_avg = sum(p['co2_impact'] for p in st.session_state.purchases[-5:]) / 5
        older_avg = sum(p['co2_impact'] for p in st.session_state.purchases[:5]) / 5
        if recent_avg < older_avg * 0.7 and "Green Champion" not in st.session_state.badges:
            st.session_state.badges.append("Green Champion")
            badges_earned.append("Green Champion")
    
    return badges_earned

# Generate badge image
def generate_badge(badge_name):
    img = Image.new('RGB', (200, 200), color=(46, 204, 113))
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    draw.ellipse([20, 20, 180, 180], fill=(39, 174, 96), outline=(255, 255, 255), width=5)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Split badge name
    words = badge_name.split()
    if len(words) >= 2:
        line1 = words[0]
        line2 = " ".join(words[1:])
        draw.text((100, 85), line1, fill=(255, 255, 255), font=font, anchor="mm")
        draw.text((100, 115), line2, fill=(255, 255, 255), font=font, anchor="mm")
    else:
        draw.text((100, 100), badge_name, fill=(255, 255, 255), font=font, anchor="mm")
    
    return img

# Eco tips
ECO_TIPS = [
    "Choose local produce to reduce transportation emissions",
    "Opt for digital receipts instead of paper ones",
    "Bring your own reusable bags when shopping",
    "Look for products with minimal packaging",
    "Support brands with transparent sustainability practices",
    "Consider buying second-hand items",
    "Repair items instead of replacing them",
    "Choose energy-efficient appliances",
    "Buy in bulk to reduce packaging waste",
    "Opt for plant-based alternatives when possible"
]

# App title and header
st.title("🌱 ShopImpact - Gamified Conscious Shopping Dashboard")
st.markdown("Track your purchases, understand your environmental impact, and earn rewards for sustainable choices!")

# Sidebar for purchase logging
with st.sidebar:
    st.header("🛒 Log New Purchase")
    
    product = st.text_input("Product Name")
    category = st.selectbox("Category", list(CO2_MULTIPLIERS.keys()))
    brand = st.text_input("Brand (Optional)")
    price = st.number_input("Price ($)", min_value=0.0, step=0.01)
    purchase_date = st.date_input("Purchase Date", datetime.now())
    
    if st.button("Add Purchase", type="primary"):
        if product and price > 0:
            # Calculate CO₂ impact
            co2_impact = round(price * CO2_MULTIPLIERS[category], 2)
            
            # Calculate XP
            xp_earned = calculate_xp(co2_impact)
            
            # Update streak
            current_date = purchase_date
            if st.session_state.last_purchase_date:
                days_diff = (current_date - st.session_state.last_purchase_date).days
                if days_diff == 1 and co2_impact < 10:
                    st.session_state.eco_streak += 1
                elif days_diff > 1:
                    st.session_state.eco_streak = 1 if co2_impact < 10 else 0
                else:
                    if co2_impact < 10:
                        st.session_state.eco_streak = max(1, st.session_state.eco_streak)
            else:
                st.session_state.eco_streak = 1 if co2_impact < 10 else 0
            
            st.session_state.last_purchase_date = current_date
            
            # Add purchase
            purchase = {
                'date': purchase_date,
                'product': product,
                'category': category,
                'brand': brand,
                'price': price,
                'co2_impact': co2_impact,
                'xp_earned': xp_earned
            }
            st.session_state.purchases.append(purchase)
            
            # Update XP and level
            st.session_state.current_xp += xp_earned
            update_level()
            
            # Check for badges
            new_badges = check_badges()
            
            st.success(f"Purchase added! CO₂ Impact: {co2_impact} kg | XP Earned: {xp_earned}")
            
            if new_badges:
                st.balloons()
                for badge in new_badges:
                    st.success(f"🎉 New Badge Unlocked: {badge}!")
        else:
            st.error("Please fill in all required fields.")

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_co2 = sum(p['co2_impact'] for p in st.session_state.purchases) if st.session_state.purchases else 0
    st.metric("🌍 Total CO₂ Impact", f"{total_co2} kg")

with col2:
    st.metric("⭐ Current XP", st.session_state.current_xp)

with col3:
    st.metric("🏆 Current Level", st.session_state.level)

with col4:
    st.metric("🔥 Eco Streak", f"{st.session_state.eco_streak} days")

# Progress bar for next level
if st.session_state.level < 4:
    current_level_xp = LEVEL_THRESHOLDS[st.session_state.level]
    next_level_xp = LEVEL_THRESHOLDS[st.session_state.level + 1]
    xp_progress = st.session_state.current_xp - current_level_xp
    xp_needed = next_level_xp - current_level_xp
    progress_percent = (xp_progress / xp_needed) * 100
    
    st.progress(min(progress_percent / 100, 1.0))
    st.caption(f"Progress to Level {st.session_state.level + 1}: {xp_progress}/{xp_needed} XP")

# Badges display
st.subheader("🏅 Your Achievements")
if st.session_state.badges:
    cols = st.columns(len(st.session_state.badges))
    for idx, badge in enumerate(st.session_state.badges):
        with cols[idx]:
            badge_img = generate_badge(badge)
            st.image(badge_img, caption=badge)
else:
    st.info("No badges yet. Make sustainable purchases to earn badges!")

# Weekly CO₂ Chart
st.subheader("📊 Weekly CO₂ Impact")
if st.session_state.purchases:
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.purchases)
    df['date'] = pd.to_datetime(df['date'])
    
    # Get last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Filter and group by day
    weekly_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    if not weekly_data.empty:
        daily_co2 = weekly_data.groupby(weekly_data['date'].dt.date)['co2_impact'].sum()
        st.bar_chart(daily_co2)
    else:
        st.info("No purchases in the last 7 days.")
else:
    st.info("Log your first purchase to see your impact chart.")

# Eco Goal Tracker
st.subheader("🎯 Monthly Eco Goal")
monthly_goal = st.slider("Set your monthly CO₂ budget (kg)", 50, 500, 200)
monthly_co2 = sum(p['co2_impact'] for p in st.session_state.purchases 
                  if p['date'].month == datetime.now().month) if st.session_state.purchases else 0
remaining_budget = max(0, monthly_goal - monthly_co2)

col1, col2 = st.columns(2)
with col1:
    st.metric("Monthly CO₂ Used", f"{monthly_co2} kg")
with col2:
    st.metric("Remaining Budget", f"{remaining_budget} kg")

# Green Future Simulator
st.subheader("🌿 Green Future Simulator")
st.markdown("See how much CO₂ you could save by choosing greener alternatives!")

if st.session_state.purchases:
    total_current = sum(p['co2_impact'] for p in st.session_state.purchases)
    
    # Calculate potential savings (30% reduction for high-impact items)
    potential_savings = 0
    for purchase in st.session_state.purchases:
        if purchase['co2_impact'] > 10:  # High impact items
            potential_savings += purchase['co2_impact'] * 0.3
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Total CO₂", f"{total_current} kg")
    with col2:
        st.metric("Potential Savings", f"{potential_savings:.1f} kg")
    
    if potential_savings > 0:
        st.info(f"💡 You could reduce your impact by {potential_savings:.1f} kg by choosing greener alternatives for high-impact purchases!")
else:
    st.info("Add some purchases to see your potential savings.")

# Purchase History
st.subheader("📝 Purchase History")
if st.session_state.purchases:
    df = pd.DataFrame(st.session_state.purchases)
    df['date'] = pd.to_datetime(df['date']).dt.date
    st.dataframe(df[['date', 'product', 'category', 'price', 'co2_impact', 'xp_earned']], 
                 use_container_width=True)
    
    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Purchase History (CSV)",
        data=csv,
        file_name="shopimpact_purchase_history.csv",
        mime="text/csv",
    )
else:
    st.info("No purchases logged yet. Add your first purchase using the sidebar!")

# Random Eco Tip
st.subheader("💡 Daily Eco Tip")
random_tip = random.choice(ECO_TIPS)
st.info(f"**{random_tip}**")

# Footer
st.markdown("---")
st.markdown("### 🌍 Shop Responsibly, Make an Impact!")
st.markdown("""
**How it works:**
- Each purchase has an estimated CO₂ impact based on its category
- Lower CO₂ impact = More XP earned
- Maintain eco-streaks by making low-impact purchases consecutively
- Earn badges for sustainable shopping habits
- Set and track your monthly eco-goals
""")

# Reset button (for development/testing)
with st.expander("⚙️ Developer Options"):
    if st.button("Reset All Data"):
        st.session_state.purchases = []
        st.session_state.current_xp = 0
        st.session_state.level = 1
        st.session_state.eco_streak = 0
        st.session_state.last_purchase_date = None
        st.session_state.badges = []
        st.rerun()
