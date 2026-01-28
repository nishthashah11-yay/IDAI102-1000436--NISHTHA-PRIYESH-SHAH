# ShopImpact – Conscious Shopping & CO₂ Awareness System  

## Project Overview  
This platform is a web-based application created with Streamlit that guides individuals toward environmentally responsible buying by recording consumption patterns and computing carbon output.  

Every item entered by a user is transformed into measurable sustainability indicators through instant processing, visual panels, and reward-based mechanics. The focus remains on steady improvement rather than fault-based pressure, promoting mindful choices through encouragement.  

The system illustrates the full development cycle of a Python-driven interactive product, covering algorithm construction, session storage, interface styling, graphical reporting, and online hosting. Its structure makes it ideal for coursework evaluation, innovation contests, and practical demonstrations.  

---

## Problem Statement  

- Ecological consequences remain hidden during transactions  
- Green habits lack motivation and response systems  
- Environmental statistics appear complex and difficult to interpret  

ShopImpact provides:  

- Conversion of buying activity into readable carbon values  
- Positive reinforcement using achievement-based mechanics  
- Clear presentation through a simplified digital layout  

---

## System Integration & Architecture  

### Data Handling and State Management  

- Transaction records  
- Daily emission totals  
- Expense monitoring  
- Sustainable action counts, continuity tracking, and achievement levels  

Efficient in-memory collections enable rapid grouping and computation.  

### Logic and Calculations  

- Emission estimation relies on category-specific intensity factors  
- Environment-friendly selections automatically apply a percentage reduction  
- Independent Python modules manage:  
  - Entry registration  
  - Footprint computation  
  - Continuity monitoring  
  - Achievement activation  
  - Periodic reporting  

### User Interface  

- Overview screen  
- Statistical review  
- Achievement gallery  
- Inspiration and insight section  
- Configuration panel  

Visual styling includes:  

- Bright and dim display modes  
- Color emphasis  
- Layout clarity and nature-inspired appearance  

### Visualization and Export  

- Structured data frames for processing  
- Graphical components for emission trends  
- Downloadable reports for analysis and documentation  

---

## Deployment  

### Local Deployment  

```bash
git clone <repository-url>
cd ShopImpact
pip install -r requirements.txt
streamlit run app.py
