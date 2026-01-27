#  ShopImpact – Gamified Conscious Shopping Dashboard

##  Project Overview  
ShopImpact is an interactive **Python + Streamlit web application** that helps users understand and reflect on the **environmental impact of their shopping habits** through visualization and gamification.  

By logging everyday purchases, users can instantly view their estimated CO₂ footprint, earn experience points (XP), unlock achievement badges, track eco-streaks, and explore how choosing greener alternatives can reduce their environmental impact.

The project promotes **conscious consumerism** in a positive, engaging, and non-judgmental way.

---

##  Problem Statement  
Most consumers are unaware of the environmental cost of everyday products, and sustainability data is often difficult to interpret.

ShopImpact addresses this by:
- Making environmental impact **visible and measurable**
- Encouraging **small, sustainable behavior changes**
- Turning eco-friendly actions into a **rewarding and motivating experience**

---

##  Target Users  
- Students and young adults  
- Environmentally conscious families  
- Beginners learning Python and data-driven applications  
- Anyone interested in reducing their carbon footprint  

---

##  Key Features  

###  Core Functionality  
- Log purchases with **product type, brand, price, and date**  
- **Real-time CO₂ impact calculation** using category-based multipliers  
- Persistent purchase history using session state  

###  Gamification System  
- **XP-based level system** (Level 1 to Level 4)  
- **Eco streak tracking** for consecutive sustainable choices  
- **Achievement badges**:  
  -  Eco Saver – Low total CO₂ impact  
  -  Conscious Consumer – Majority low-impact purchases  
  -  Sustainability Streaker – 5-day eco streak  
  -  Green Champion – Impact reduced over time  
- Visual **eco badge generated using Python (PIL)**  
- Progress bar showing advancement toward the next level  

###  Visual Dashboard  
- Total CO₂ impact  
- Current XP and Level  
- Streak counter  
- Weekly CO₂ impact bar chart  
- Purchase history table  

###  Sustainability Tools  
- **Monthly Eco Goal Tracker** with remaining carbon budget  
- **Green Future Simulator** to estimate CO₂ reduction if users switch to greener alternatives  
- Random **eco tips** for positive reinforcement  
- CSV download of purchase history  

---

##  Python Concepts Used  
- Lists and dictionaries for structured data storage  
- Functions and conditional logic for calculations and rewards  
- Session state for persistent user interaction  
- Date and time handling for streaks and weekly analysis  
- Data analysis using Pandas  
- Image generation using Pillow (PIL)  
- Data visualization using Streamlit charts  

---

##  Technologies Used  
- **Python 3**  
- **Streamlit** – interactive web interface  
- **Pandas** – data handling and charts  
- **Pillow (PIL)** – badge graphics  
- **Datetime module** – time-based analytics  

---

##  Project Structure  

```text
ShopImpact/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

#  Project Development Stages

###  Stage 1: Planning & Design
The planning phase focused on identifying target users, pain points, and key features. A mind map was created to visualize user needs and interactions, followed by low-fidelity wireframes to establish layout, input flow, and dashboard structure.

![Mindmap](assets/stage1/mindmap.png)  
*Figure 1: Project Mindmap*

![Wireframe](assets/stage1/wireframe.png)  
*Figure 2: Low-fidelity UI Wireframe*

###  Stage 2: Build the Python Logic
Designed a list of dictionaries to store purchase data
Applied category-based CO₂ multipliers for environmental impact calculation
Built modular functions for:
Impact calculation
XP and level progression
Badge unlocking
Streak tracking
Integrated session state for persistent user interaction across app reloads

###  Stage 3: Interactive Interface
The interface was refined iteratively based on usability testing and visual clarity.
Screenshots below show the finalized interface used for deployment.

#### 📸 Interface Screenshots (Final UI)

| Dashboard Overview | Purchase Logging |
|-------------------|------------------|
| ![Dashboard](assets/screenshots/ui_dashboard.png) | ![Purchase](assets/screenshots/ui_purchase.png) |

| Gamification Panel | Badge System |
|-------------------|--------------|
| ![Gamification](assets/screenshots/ui_gamification.png) | ![Badges](assets/screenshots/ui_badges.png) |

| Weekly Analytics | Turtle Avatar |
|-----------------|---------------|
| ![Analytics](assets/screenshots/ui_weekly.png) | ![Turtle](assets/screenshots/ui_turtle.png) |

**Note:** The Eco Feedback Panel persistently displays greener alternatives and eco tips based on the user’s most recent purchase, ensuring alignment between the planned wireframe and final interface.

*Figure 3: Final ShopImpact interface showing dashboard metrics, purchase logging, gamification elements, badge system, weekly analytics, and the symbolic turtle avatar.*

###  Stage 4: Testing & Gamification

Testing was conducted using 15 unique purchase scenarios to validate badge unlocking rules, point accumulation accuracy, and overall dashboard calculations.

![Testing](assets/stage4/testing_1.png)  

During testing, the badge logic was refined to ensure rewards were based on environmental efficiency and improvement rather than purchase quantity, aligning the gamification system with sustainability principles.

| Before | After |
|-------------------|------------------|
| ![Badges](assets/stage4/badges.png)  | ![Badges](assets/stage4/badges_after.png)  |

In addition to functional testing, informal usability testing was carried out with peers to assess clarity of navigation, readability of metrics, and overall user experience. Based on this feedback, badge visuals were simplified for better recognition, and a weekly impact chart was introduced to improve trend visibility and user understanding.

###  Stage 5: Deployment
The finalized application was deployed on **Streamlit Cloud**, ensuring accessibility for users across different devices. Dependencies were managed via `requirements.txt` to guarantee a consistent runtime environment.



Run the application

streamlit run app.py

 Deployment

The application is deployed using Streamlit Cloud:

Push the project to GitHub

Visit https://streamlit.io/cloud

Click New App

Connect your repository

Select app.py as the main file

Click Deploy

 Testing

Logged 15+ purchases across all categories

Verified XP, levels, and badge unlocking logic

Tested eco-streak increment and reset

Confirmed weekly chart accuracy

Validated eco-goal and green-simulator calculations

Ensured CSV export and dashboard stability

 Ethical & Social Impact

CO₂ values are simplified estimates for educational purposes

No fear-based or guilt-driven messaging

Rewards are based on better choices, not more consumption

Encourages responsible and mindful shopping habits

 Student Details

Student Name: Nishtha Priyesh Shah

Student ID: 1000436

Course: Artificial Intelligence

Subject: Python Programming

Assessment Type: Summative Assessment

Institution: Aspee Nutan Academy

 Conclusion

ShopImpact demonstrates how Python can be used to design a complete, real-world, interactive system that combines data analysis, visualization, and gamification for social good. The project highlights the full development cycle—from problem identification and logic design to deployment—while promoting sustainability through positive digital engagement.

Track • Reflect • Improve • Shop Responsibly 🌍
