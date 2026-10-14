# AgriCycle: Agricultural Waste Management & Eco-Friendly Fertilizer Platform

A full-stack, sustainable agricultural platform designed to eliminate open crop residue burning, divert organic farm waste from landfills, and convert biomass into certified eco-friendly fertilizers (vermicompost, biochar, bio-inoculants, and fermented liquid nutrients).

---

## 🎯 Alignment with Problem Statement & Key Objectives

| Key Objective | Platform Implementation |
| :--- | :--- |
| **Waste Reduction** | Doorstep agricultural waste collection logistics module for paddy straw, wheat stubble, bagasse, and cattle manure with real-time status tracking. |
| **Eco-Friendly Fertilizer Production** | Scientific Composting Lab featuring an interactive Carbon-to-Nitrogen (C:N) ratio calculator and IoT telemetry batch tracker. |
| **Environmental Protection** | Live metric engine calculating CO₂ emissions averted (1.46 kg CO₂e / kg biomass burned) and landfill diversion. |
| **Soil Improvement** | Intelligent Soil Health Advisor formulating crop-specific organic nutrient regimes for clayey, sandy, alluvial, and saline soils. |
| **Cost-Effectiveness** | Direct-to-farmer marketplace for vermicompost and biofertilizers, cutting chemical fertilizer expenditure by 30–40%. |
| **Circular Agriculture** | Closed-loop system connecting crop residue collection directly with organic fertilizer synthesis and distribution. |

---

## 🚀 Key Modules & Features

### 1. 📊 Central Impact Dashboard
- **Live Metrics**: Displays total biomass diverted (Tons), CO₂ emissions averted (Tons), organic fertilizer produced (Tons), and farming clusters enrolled.
- **Bioconversion Impact Flow**: Interactive Chart.js graph tracking agricultural waste intake vs. fertilizer output across crop categories.
- **Active Bioreactor Monitor**: Telemetry tracking temperature (°C), moisture (%), and stage for active vermiculture pits and windrow piles.

### 2. 🚜 Waste Collection & Logistics
- Farmers can submit pickup bookings specifying residue type (paddy straw, wheat stubble, sugarcane bagasse, cattle manure, coir pith), quantity (kg), and farm coordinates.
- Transparent lifecycle tracking: `Pending Collection` ➔ `Scheduled for Pickup` ➔ `In Bio-Conversion` ➔ `Converted to Fertilizer`.

### 3. 🧪 Composting & Vermicomposting Lab
- **C:N Ratio Balancing Engine**: Accurately computes weighted Carbon-to-Nitrogen ratios between Nitrogen "greens" (cow dung slurry, poultry manure, green weeds) and Carbon "browns" (paddy straw, sawdust, bagasse).
- Gives immediate feedback on whether the mix meets the optimal 25:1–30:1 golden composting zone, calculates required corrective weights, and predicts compost yield.
- Detailed guidelines on *Eisenia foetida* vermiculture management and moisture regulation (55–60%).

### 4. 🛍️ Eco-Friendly Fertilizer Marketplace
- Catalog of certified organic inputs:
  - **Organic Vermicompost Gold** (Pure castings enriched with humic acid)
  - **Enriched Biochar & Stubble Compost** (Long-term soil carbon sequestration)
  - **Rhizo-Azoto Microbial Inoculant** (Atmospheric N-fixer & P-solubilizer)
  - **Fermented Jeevamrutha** (Liquid bio-enhancer consortium)
  - **Phospho-Compost** (Rock phosphate co-composted with agricultural biomass)
- Direct order placement with real-time total price calculation.

### 5. 🔬 Soil Health Advisor & Fertilizer Formulator
- Calibrates custom organic fertilizer dosages based on soil type (Alluvial, Black cotton, Red sandy loam, Heavy clay, Saline) and target crop (Paddy, Wheat, Cotton, Vegetables, Pulses, Sugarcane).
- Estimates chemical fertilizer replacement rate (30–35% reduction in synthetic Urea and DAP) and calculated monetary savings.

### 6. 📖 Educational Knowledge Hub
- Detailed comparison between open burning hazards (PM2.5, microbial sterilization) and bioconversion benefits.
- 4-step Standard Operating Procedure (SOP) for setting up rural vermicomposting pits.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy (ORM)
- **Database**: SQLite (`agri_waste.db`)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, FontAwesome 6
- **Data Visualization**: Chart.js

---

## 💻 Installation & Running Locally

### 1. Prerequisites
- Python 3.10+ installed

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```
*(The SQLite database and demo data are auto-generated and seeded upon the first run).*

---

## 📂 Project Structure

```
Agriculture Waste Management/
├── app.py                      # Core Flask application, routing, and APIs
├── models.py                   # SQLAlchemy ORM models
├── seed_data.py                # Initial database seeder
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation and problem statement alignment
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling and color themes
│   └── js/
│       └── main.js             # Client-side UI enhancements
└── templates/
    ├── base.html               # Shared layout and navigation
    ├── index.html              # Dashboard with impact analytics and charts
    ├── waste_collection.html   # Waste pickup scheduling & status tracking
    ├── composting_lab.html     # C:N calculator & bioreactor telemetry
    ├── marketplace.html        # Fertilizer catalog with order modal
    ├── orders.html             # Order history & dispatch tracker
    ├── soil_advisor.html       # Soil diagnostic & fertilizer recommender
    └── guide.html              # Educational handbook and circular economy SOP
```
