import streamlit as st
from datetime import datetime
import random
import pandas as pd
import time
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import turtle
import tempfile


st.set_page_config(page_title="🌱 EcoImpact Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
}

h1, h2, h3 {
    color: #2E7D32 !important;
    font-weight: 700 !important;
}

h1 {
    background: linear-gradient(90deg, #1B5E20, #4CAF50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 3rem !important;
    margin-bottom: 0.5rem !important;
    font-family: 'Montserrat', sans-serif;
}

.stButton>button {
    background: linear-gradient(90deg, #2E7D32, #4CAF50);
    color: white;
    border: none;
    padding: 14px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(46, 125, 50, 0.25);
    width: 100%;
    position: relative;
    overflow: hidden;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(46, 125, 50, 0.35);
}

.stButton>button:active {
    transform: translateY(-1px);
}

.stSelectbox, .stTextInput, .stNumberInput {
    border: 2px solid #C8E6C9 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    transition: all 0.3s ease;
}

.stSelectbox:focus, .stTextInput:focus, .stNumberInput:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1) !important;
}

.metric-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1);
    border: 1px solid #E8F5E9;
    transition: all 0.3s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(76, 175, 80, 0.15);
}

.stProgress > div > div {
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
    border-radius: 10px;
}

.eco-badge {
    animation: float 4s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-15px) rotate(5deg); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes slideIn {
    from { transform: translateX(-100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.quote-box {
    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #4CAF50;
    font-style: italic;
    margin: 15px 0;
    animation: slideIn 0.5s ease;
}

.tip-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 2px dashed #A5D6A7;
    margin: 10px 0;
    animation: pulse 2s infinite;
}

.achievement-card {
    background: linear-gradient(135deg, #FFF8E1, #FFECB3);
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    text-align: center;
    animation: pulse 3s infinite;
    border: 2px solid #FFD600;
}

.streak-fire {
    animation: pulse 1s infinite;
    color: #FF5722;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #ffffff 0%, #f8fff8 100%);
    border-right: 2px solid #E8F5E9;
}

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E8F5E9;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.download-btn {
    background: linear-gradient(90deg, #2196F3, #21CBF3);
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.download-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3);
}

.feedback-box {
    background: linear-gradient(135deg, #E3F2FD, #E1F5FE);
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #2196F3;
    margin-top: 20px;
}

.turtle-container {
    background: #F0F9F0;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #C8E6C9;
}
</style>
""", unsafe_allow_html=True)

if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "total_impact" not in st.session_state:
    st.session_state.total_impact = 0
if "achievements" not in st.session_state:
    st.session_state.achievements = []
if "last_login" not in st.session_state:
    st.session_state.last_login = datetime.now().date()
    st.session_state.daily_tip_seen = False
    st.session_state.current_tip = None
if "current_tip" not in st.session_state:
    st.session_state.current_tip = None

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
    "Green choices today, brighter world tomorrow",
    "You're not just shopping—you're voting for the planet",
    "Every rupee spent wisely is a leaf on the tree of life",
    "Your eco-streak is heating up! Keep going!",
    "Small steps, massive impact—you're making history!"
]

ECO_TIPS = [
    "Always carry reusable shopping bags",
    "Use a refillable water bottle instead of plastic",
    "Walk or cycle for short distance shopping",
    "Choose products with minimal packaging",
    "Buy local to reduce transportation emissions",
    "Always separate recyclables from trash",
    "Plan meals to reduce food waste",
    "Switch to LED bulbs at home",
    "Bring your own coffee cup",
    "Support brands that plant trees",
    "Install water-saving showerheads",
    "Use cloth napkins instead of paper",
    "Unplug chargers when not in use",
    "Wash clothes in cold water",
    "Use natural light during daytime",
    "Repair items instead of replacing",
    "Eat more plant-based meals",
    "Borrow books instead of buying",
    "Give experiences instead of physical gifts",
    "Plant native species in your garden"
]

ACHIEVEMENTS = [
    "First Green Purchase",
    "3-Day Eco Streak",
    "5 Eco Purchases",
    "Carbon Saver",
    "Planet Protector",
    "Impact Champion",
    "Earth Guardian"
]

def generate_turtle_animation(score):
    img = Image.new('RGB', (300, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    badge_colors = [(46, 125, 50), (56, 142, 60), (76, 175, 80), (102, 187, 106), (129, 199, 132)]
    color_idx = min(len(badge_colors)-1, score // 20)
    
    center_x, center_y = 150, 150
    radius = 100
    
    for i in range(radius, 0, -5):
        color_ratio = i / radius
        r = int(badge_colors[color_idx][0] * color_ratio)
        g = int(badge_colors[color_idx][1] * color_ratio)
        b = int(badge_colors[color_idx][2] * color_ratio)
        draw.ellipse([center_x-i, center_y-i, center_x+i, center_y+i], 
                    fill=(r, g, b), outline=(200, 230, 200))
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    draw.text((150, 130), "ECO", fill=(255, 255, 255), anchor="mm", font=font_large)
    draw.text((150, 180), f"{score}/100", fill=(255, 255, 255), anchor="mm", font=font_small)
    
    for i in range(5):
        angle = i * 72
        x = center_x + (radius-20) * np.cos(np.radians(angle))
        y = center_y + (radius-20) * np.sin(np.radians(angle))
        
        points = []
        for j in range(5):
            point_angle = angle + j * 72
            px = x + 15 * np.cos(np.radians(point_angle))
            py = y + 15 * np.sin(np.radians(point_angle))
            points.append((px, py))
        
        draw.polygon(points, fill=(255, 215, 0), outline=(255, 193, 7))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return buf

def create_turtle_progress(progress_percentage):
    # Convert to integer to avoid float indexing error
    progress_percentage = int(min(100, max(0, progress_percentage)))
    
    img = Image.new('RGB', (700, 150), color=(240, 249, 240))
    draw = ImageDraw.Draw(img)
    
    track_start = 50
    track_end = 650
    track_y = 75
    
    draw.rectangle([track_start-5, track_y-10, track_end+5, track_y+10], 
                   fill=(200, 230, 200), outline=(165, 214, 167), width=2)
    
    progress_width = int((track_end - track_start) * (progress_percentage / 100))
    draw.rectangle([track_start, track_y-8, track_start + progress_width, track_y+8], 
                   fill=(76, 175, 80), outline=(56, 142, 60), width=2)
    
    for i in range(0, 101, 20):
        x = track_start + int((track_end - track_start) * (i / 100))
        draw.line([x, track_y-15, x, track_y+15], fill=(129, 199, 132), width=2)
        draw.text((x, track_y+25), f"{i}%", fill=(46, 125, 50), anchor="mt", 
                  font=ImageFont.load_default())
    
    turtle_x = track_start + progress_width - 20
    turtle_y = track_y
    
    # Call draw_turtle with the same progress_percentage
    draw_turtle(draw, turtle_x, turtle_y, progress_percentage)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return buf

def draw_turtle(draw, x, y, progress):
    turtle_colors = [(139, 195, 74), (104, 159, 56), (85, 139, 47), (67, 160, 71), (56, 142, 60)]
    
    # Ensure progress is integer for list indexing
    progress = int(progress)
    color_idx = min(len(turtle_colors)-1, progress // 20)
    shell_color = turtle_colors[color_idx]
    
    shell_size = 20
    draw.ellipse([x-shell_size, y-shell_size, x+shell_size, y+shell_size], 
                 fill=shell_color, outline=(56, 142, 60), width=2)
    
    head_size = 12
    draw.ellipse([x+shell_size-5, y-head_size//2, x+shell_size+head_size-5, y+head_size//2], 
                 fill=shell_color, outline=(56, 142, 60), width=1)
    
    eye_size = 3
    draw.ellipse([x+shell_size+head_size-10, y-2, x+shell_size+head_size-6, y+2], 
                 fill=(0, 0, 0))
    
    legs = [
        (x-15, y-15, x-5, y-5),
        (x-15, y+15, x-5, y+5),
        (x+5, y-15, x+15, y-5),
        (x+5, y+15, x+15, y+5)
    ]
    
    for leg in legs:
        draw.line(leg, fill=(67, 160, 71), width=3)
    
    tail_length = 15
    draw.line([x-shell_size, y, x-shell_size-tail_length, y], 
              fill=(67, 160, 71), width=3)
def save_feedback(name, email, rating, feedback):
    try:
        feedback_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': name,
            'email': email,
            'rating': rating,
            'feedback': feedback
        }
        
        with open('feedback.txt', 'a', encoding='utf-8') as f:
            f.write(f"Timestamp: {feedback_data['timestamp']}\n")
            f.write(f"Name: {feedback_data['name']}\n")
            f.write(f"Email: {feedback_data['email']}\n")
            f.write(f"Rating: {feedback_data['rating']}/5\n")
            f.write(f"Feedback: {feedback_data['feedback']}\n")
            f.write("-" * 50 + "\n")
        
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")
        return False

def download_purchase_history():
    if st.session_state.purchases:
        # Create a clean version without emojis from all columns
        clean_data = []
        for purchase in st.session_state.purchases:
            clean_row = {}
            for key, value in purchase.items():
                clean_value = value
                # Remove ₹ symbol from Price column
                if key == "Price":
                    clean_value = str(value).replace("₹", "")
                # Clean Type column
                elif key == "Type":
                    if str(value) == "🌱 Eco":
                        clean_value = "Eco"
                    elif str(value) == "🛍️ Regular":
                        clean_value = "Regular"
                    else:
                        clean_value = str(value).replace("🌱", "Eco").replace("🛍️", "Regular")
                # Ensure all values are strings for consistency
                clean_row[key] = str(clean_value)
            clean_data.append(clean_row)
        
        df = pd.DataFrame(clean_data)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a class="download-btn" href="data:file/csv;base64,{b64}" download="eco_purchase_history.csv">📥 Download Purchase History</a>'
        return href
    return None

st.title("🌱 EcoImpact Pro")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
Track Your Shopping Impact • Grow Your Eco-Streak • Save Our Planet
</div>
""", unsafe_allow_html=True)

current_date = datetime.now().date()
if current_date != st.session_state.last_login:
    st.session_state.streak += 1
    st.session_state.last_login = current_date
    st.session_state.daily_tip_seen = False
    if st.session_state.streak % 3 == 0:
        achievement = random.choice(ACHIEVEMENTS)
        if achievement not in st.session_state.achievements:
            st.session_state.achievements.append(achievement)

if st.session_state.current_tip is None:
    st.session_state.current_tip = random.choice(ECO_TIPS)

col_header1, col_header2, col_header3 = st.columns([2, 1, 1])

with col_header1:
    st.markdown(f"<div class='quote-box'>🌍 {random.choice(MOTIVATIONAL_QUOTES)}</div>", unsafe_allow_html=True)

with col_header2:
    st.markdown(f"### <span class='streak-fire'>🔥 Day {st.session_state.streak}</span>", unsafe_allow_html=True)

with col_header3:
    st.markdown(f"<div class='tip-card'>💡 Tip: {st.session_state.current_tip}</div>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Log Your Purchase")
    
    with st.form("purchase_form"):
        product_type = st.selectbox("Category", list(IMPACT_MULTIPLIER.keys()))
        brand = st.text_input("Brand/Store Name", placeholder="e.g., Local Market, Brand Name")
        price = st.number_input("Price (₹)", min_value=1, value=100)
        
        col_submit1, col_submit2 = st.columns(2)
        with col_submit1:
            submit_normal = st.form_submit_button("🛍️ Add Purchase")
        with col_submit2:
            submit_eco = st.form_submit_button("🌱 Eco Purchase")
    
    if submit_normal or submit_eco:
        if not brand:
            st.warning("Please enter a brand/store name!")
        else:
            is_eco = (submit_eco or product_type in ["Second-hand", "Eco-Friendly"])
            multiplier = IMPACT_MULTIPLIER.get(product_type, 0.3)
            if is_eco:
                multiplier *= 0.5
            
            impact = price * multiplier
            
            st.session_state.purchases.append({
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Category": product_type,
                "Brand": brand,
                "Price": f"₹{price}",
                "Impact": f"{impact:.1f}",
                "Type": "🌱 Eco" if is_eco else "🛍️ Regular"
            })
            
            st.session_state.total_impact += impact
            
            if is_eco:
                st.session_state.streak += 1
                st.success(f"""
                🎉 Amazing Eco Choice! 
                +1 to your streak! (Now: {st.session_state.streak} days)
                """)
                st.balloons()
                
                if len([p for p in st.session_state.purchases if "🌱" in p.get("Type", "")]) % 3 == 0:
                    new_achievement = random.choice(ACHIEVEMENTS)
                    if new_achievement not in st.session_state.achievements:
                        st.session_state.achievements.append(new_achievement)
                        st.success(f"🏆 New Achievement Unlocked: {new_achievement}!")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Your Impact Dashboard")
    
    if st.session_state.purchases:
        total_spent = sum(int(p["Price"].replace("₹", "")) for p in st.session_state.purchases)
        eco_score_val = max(0, min(100, 100 - (st.session_state.total_impact / max(1, total_spent)) * 100))
        
        col_metrics1, col_metrics2 = st.columns(2)
        with col_metrics1:
            st.metric("💰 Total Spent", f"₹{total_spent:,}")
            st.metric("🌱 Eco Score", f"{int(eco_score_val)}/100")
        with col_metrics2:
            st.metric("🌍 CO₂ Impact", f"{st.session_state.total_impact:.1f}")
            st.metric("🛒 Purchases", len(st.session_state.purchases))
        
        st.markdown("#### 📈 Turtle Progress Tracker")
        progress_img = create_turtle_progress(eco_score_val)
        st.image(progress_img, width=700)
        
        st.markdown("#### 🏆 Your Eco Badge")
        badge_img = generate_turtle_animation(int(eco_score_val))
        st.image(badge_img, width=200)
        
        if st.session_state.achievements:
            st.markdown("#### 🎖️ Achievements")
            cols = st.columns(3)
            for idx, achievement in enumerate(st.session_state.achievements[-6:]):
                with cols[idx % 3]:
                    st.markdown(f"<div class='achievement-card'>🏆 {achievement}</div>", 
                               unsafe_allow_html=True)
    else:
        st.info("🌟 Start your eco-journey by logging your first purchase!")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

col3, col4 = st.columns([2, 1])

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 📋 Purchase History")
    
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases[-10:])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        download_link = download_purchase_history()
        if download_link:
            st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.info("No purchases logged yet. Your eco-story begins here!")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 🌳 Future Simulator")
    
    eco_percentage = st.slider("Target % of Eco Purchases", 0, 100, 50, 5)
    
    if st.session_state.purchases:
        potential_savings = st.session_state.total_impact * (eco_percentage / 100) * 0.35
        
        trees_saved = potential_savings / 21.77
        st.success(f"""
        🌟 Potential Impact:
        - CO₂ Reduction: {potential_savings:.1f} units
        - Equivalent to {trees_saved:.1f} trees
        """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='feedback-box'>", unsafe_allow_html=True)
st.markdown("### 📝 Feedback Form")
st.markdown("Help us improve EcoImpact Pro! Share your thoughts and suggestions.")

with st.form("feedback_form"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        name = st.text_input("Your Name")
    with col_f2:
        email = st.text_input("Your Email (optional)", placeholder="email@example.com")
    
    rating = st.slider("Rate your experience (1-5 stars)", 1, 5, 4)
    
    feedback = st.text_area("Your Feedback", 
                          placeholder="What do you like about EcoImpact Pro? How can we improve?",
                          height=100)
    
    submitted = st.form_submit_button("Submit Feedback 💚")
    
    if submitted:
        if not name:
            st.warning("Please enter your name!")
        elif not feedback:
            st.warning("Please share your feedback!")
        else:
            if save_feedback(name, email, rating, feedback):
                st.success("🎉 Thank you for your feedback! We appreciate your input.")
                st.balloons()
st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.sidebar.markdown("### 🌟 Quick Actions")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

if st.sidebar.button("🔄 Reset Data", use_container_width=True):
    st.session_state.purchases = []
    st.session_state.total_impact = 0
    st.session_state.achievements = []
    st.success("Data reset! Fresh start for your eco-journey!")

if st.sidebar.button("🔄 New Tip", use_container_width=True):
    st.session_state.current_tip = random.choice(ECO_TIPS)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Current Eco Tip")
st.sidebar.markdown(f"""
<div style='background: #E8F5E9; padding: 15px; border-radius: 10px; margin: 10px 0;'>
💡 {st.session_state.current_tip}
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Leaderboard")
st.sidebar.metric("Your Rank", f"#{random.randint(1, 50)}")
st.sidebar.metric("Global Impact", f"{random.randint(10000, 50000):,} kg CO₂ saved")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<h3>🌍 Together, We Can Make a Difference</h3>
<p>Every conscious choice brings us closer to a sustainable future. Keep tracking, keep improving!</p>
<p style='font-size: 0.9rem; margin-top: 20px;'>EcoImpact Pro • Made with 💚 for our Planet</p>
</div>
""", unsafe_allow_html=True)
