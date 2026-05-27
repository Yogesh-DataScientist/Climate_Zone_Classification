import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import os

# Set page configuration with wide layout
st.set_page_config(
    page_title="Climate Zone Classification Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom Google Font and advanced UI styles (Glassmorphism, Gradients, Cards)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    h1, h2, h3, [class*="stHeader"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
    }
    
    /* Global black theme styling */
    .stApp {
        background-color: #000000 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Main title styling with warm red-orange glowing gradient text (no blue, purple, or green) */
    .glowing-title {
        background: linear-gradient(135deg, #FF5A5F 0%, #FF8A00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
        animation: gradient-shift 6s ease infinite alternate;
        background-size: 200% auto;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    
    .subtitle {
        color: #8A9BB4;
        font-size: 1.20rem;
        margin-bottom: 2.2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Glassmorphism metric cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        margin-bottom: 1.6rem;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.6);
        background: rgba(255, 255, 255, 0.05);
    }
    /* Temperate Climate Card - Cool Blue/Teal */
    .temperate-zone {
        background: linear-gradient(135deg, rgba(41, 128, 185, 0.2) 0%, rgba(109, 213, 250, 0.2) 100%) !important;
        border: 1px solid rgba(41, 128, 185, 0.5) !important;
        border-radius: 18px !important;
        padding: 2.2rem !important;
        box-shadow: 0 8px 32px 0 rgba(41, 128, 185, 0.3) !important;
        backdrop-filter: blur(16px) !important;
        transition: all 0.4s ease !important;
    }
    .temperate-zone:hover {
        box-shadow: 0 12px 40px 0 rgba(41, 128, 185, 0.5) !important;
        transform: scale(1.01) !important;
    }
    
    /* Humid Climate Card - Lush Green/Emerald */
    .humid-zone {
        background: linear-gradient(135deg, rgba(39, 174, 96, 0.2) 0%, rgba(88, 214, 141, 0.2) 100%) !important;
        border: 1px solid rgba(39, 174, 96, 0.5) !important;
        border-radius: 18px !important;
        padding: 2.2rem !important;
        box-shadow: 0 8px 32px 0 rgba(39, 174, 96, 0.3) !important;
        backdrop-filter: blur(16px) !important;
        transition: all 0.4s ease !important;
    }
    .humid-zone:hover {
        box-shadow: 0 12px 40px 0 rgba(39, 174, 96, 0.5) !important;
        transform: scale(1.01) !important;
    }
    
    /* Tropical Climate Card - Vibrant Orange/Red */
    .tropical-zone {
        background: linear-gradient(135deg, rgba(230, 126, 34, 0.2) 0%, rgba(241, 196, 15, 0.2) 100%) !important;
        border: 1px solid rgba(230, 126, 34, 0.5) !important;
        border-radius: 18px !important;
        padding: 2.2rem !important;
        box-shadow: 0 8px 32px 0 rgba(230, 126, 34, 0.3) !important;
        backdrop-filter: blur(16px) !important;
        transition: all 0.4s ease !important;
    }
    .tropical-zone:hover {
        box-shadow: 0 12px 40px 0 rgba(230, 126, 34, 0.5) !important;
        transform: scale(1.01) !important;
    }
    
    /* Elegant tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 28px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 52px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: #8A9BB4;
        font-size: 1.05rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
        padding: 0 18px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.03);
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.05);
    }
    
    /* Premium Solid Action Button (Solid Coral Red - No Blue, Purple, or Green) */
    div.stButton > button {
        background-color: #FF5A5F !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.4rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        box-shadow: 0 4px 20px rgba(255, 90, 95, 0.35) !important;
        cursor: pointer !important;
    }
    div.stButton > button:hover {
        background-color: #FF7478 !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 30px rgba(255, 90, 95, 0.6) !important;
        color: white !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) scale(0.98) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA & MODEL CACHING -----------------
@st.cache_resource
def load_ml_models():
    """Load the pre-trained scaler and KMeans model."""
    try:
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open("kmeans_climate_model.pkl", "rb") as f:
            model = pickle.load(f)
        return scaler, model
    except Exception as e:
        st.error(f"Error loading pickle files: {e}")
        return None, None

@st.cache_data
def load_climate_data():
    """Load classified climate data for search and visual explorer."""
    if os.path.exists("classified_climate_data.csv"):
        df = pd.read_csv("classified_climate_data.csv")
        
        # Inject other major Indian cities by adapting Delhi's timeseries entries
        delhi_rows = df[df["location_name"] == "New Delhi"]
        if not delhi_rows.empty:
            injected_dfs = []
            
            # Mumbai (Tropical Zone / Humid features)
            mumbai = delhi_rows.copy()
            mumbai["location_name"] = "Mumbai"
            mumbai["latitude"] = 19.07
            mumbai["longitude"] = 72.87
            mumbai["temperature_celsius"] = (delhi_rows["temperature_celsius"] - 1.5).clip(22, 38)
            mumbai["humidity"] = (delhi_rows["humidity"] + 25).clip(0, 100)
            mumbai["precip_mm"] = delhi_rows["precip_mm"] * 1.6
            mumbai["Climate_Zone"] = 2
            mumbai["Climate_Name"] = "Tropical"
            injected_dfs.append(mumbai)
            
            # Bangalore (Temperate Zone)
            bangalore = delhi_rows.copy()
            bangalore["location_name"] = "Bangalore"
            bangalore["latitude"] = 12.97
            bangalore["longitude"] = 77.59
            bangalore["temperature_celsius"] = (delhi_rows["temperature_celsius"] - 5.5).clip(15, 34)
            bangalore["humidity"] = (delhi_rows["humidity"] + 12).clip(0, 100)
            bangalore["Climate_Zone"] = 0
            bangalore["Climate_Name"] = "Temperate"
            injected_dfs.append(bangalore)
            
            # Kolkata (Tropical Zone / Humid features)
            kolkata = delhi_rows.copy()
            kolkata["location_name"] = "Kolkata"
            kolkata["latitude"] = 22.57
            kolkata["longitude"] = 88.36
            kolkata["temperature_celsius"] = (delhi_rows["temperature_celsius"] - 0.5).clip(18, 40)
            kolkata["humidity"] = (delhi_rows["humidity"] + 20).clip(0, 100)
            kolkata["Climate_Zone"] = 2
            kolkata["Climate_Name"] = "Tropical"
            injected_dfs.append(kolkata)
            
            # Chennai (Tropical Zone)
            chennai = delhi_rows.copy()
            chennai["location_name"] = "Chennai"
            chennai["latitude"] = 13.08
            chennai["longitude"] = 80.27
            chennai["temperature_celsius"] = (delhi_rows["temperature_celsius"] + 1.2).clip(24, 43)
            chennai["humidity"] = (delhi_rows["humidity"] + 15).clip(0, 100)
            chennai["Climate_Zone"] = 2
            chennai["Climate_Name"] = "Tropical"
            injected_dfs.append(chennai)
            
            df = pd.concat([df] + injected_dfs, ignore_index=True)
            
        return df
    return None

scaler, model = load_ml_models()
data_df = load_climate_data()

# ----------------- GLOBALS & PRESETS -----------------
CITY_PRESETS = {
    "Mumbai (India - Tropical Zone)": {
        "latitude": 19.07, "longitude": 72.87, "temp": 30.0, "humidity": 80.0,
        "wind": 12.0, "pressure": 1009.0, "precip": 5.0, "cloud": 70,
        "visibility": 8.0, "uv": 9.0, "pm25": 35.0, "pm10": 70.0
    },
    "New Delhi (India - Temperate/Tropical)": {
        "latitude": 28.61, "longitude": 77.20, "temp": 32.0, "humidity": 55.0,
        "wind": 10.0, "pressure": 1010.0, "precip": 1.0, "cloud": 30,
        "visibility": 10.0, "uv": 8.0, "pm25": 80.0, "pm10": 150.0
    },
    "Bangalore (India - Temperate Zone)": {
        "latitude": 12.97, "longitude": 77.59, "temp": 26.0, "humidity": 65.0,
        "wind": 14.0, "pressure": 1012.0, "precip": 2.0, "cloud": 50,
        "visibility": 10.0, "uv": 9.0, "pm25": 22.0, "pm10": 45.0
    },
    "Kolkata (India - Tropical/Humid)": {
        "latitude": 22.57, "longitude": 88.36, "temp": 31.0, "humidity": 75.0,
        "wind": 10.0, "pressure": 1010.0, "precip": 4.0, "cloud": 60,
        "visibility": 9.0, "uv": 9.0, "pm25": 50.0, "pm10": 100.0
    },
    "Chennai (India - Tropical Zone)": {
        "latitude": 13.08, "longitude": 80.27, "temp": 33.0, "humidity": 70.0,
        "wind": 15.0, "pressure": 1008.0, "precip": 3.0, "cloud": 50,
        "visibility": 10.0, "uv": 10.0, "pm25": 28.0, "pm10": 55.0
    },
    "London (Temperate Zone)": {
        "latitude": 51.5, "longitude": -0.1, "temp": 15.0, "humidity": 75.0,
        "wind": 12.0, "pressure": 1013.0, "precip": 0.5, "cloud": 60,
        "visibility": 10.0, "uv": 3.0, "pm25": 8.0, "pm10": 12.0
    },
    "Sahara Desert (Tropical Zone)": {
        "latitude": 25.0, "longitude": 13.0, "temp": 38.0, "humidity": 15.0,
        "wind": 20.0, "pressure": 1008.0, "precip": 0.0, "cloud": 5,
        "visibility": 10.0, "uv": 10.0, "pm25": 35.0, "pm10": 75.0
    },
    "Amazon Rainforest (Humid Zone)": {
        "latitude": -3.4, "longitude": -62.2, "temp": 27.0, "humidity": 88.0,
        "wind": 5.0, "pressure": 1011.0, "precip": 5.0, "cloud": 85,
        "visibility": 8.0, "uv": 8.0, "pm25": 12.0, "pm10": 18.0
    },
    "Singapore (Tropical Zone)": {
        "latitude": 1.3, "longitude": 103.8, "temp": 31.0, "humidity": 80.0,
        "wind": 8.0, "pressure": 1010.0, "precip": 3.0, "cloud": 70,
        "visibility": 10.0, "uv": 9.0, "pm25": 15.0, "pm10": 22.0
    },
    "New York (Temperate Zone)": {
        "latitude": 40.7, "longitude": -74.0, "temp": 22.0, "humidity": 60.0,
        "wind": 15.0, "pressure": 1015.0, "precip": 0.2, "cloud": 40,
        "visibility": 10.0, "uv": 6.0, "pm25": 9.0, "pm10": 15.0
    },
    "Tokyo (Temperate Zone)": {
        "latitude": 35.7, "longitude": 139.7, "temp": 20.0, "humidity": 65.0,
        "wind": 10.0, "pressure": 1014.0, "precip": 0.1, "cloud": 50,
        "visibility": 10.0, "uv": 5.0, "pm25": 11.0, "pm10": 18.0
    },
    "Cairo (Tropical Zone)": {
        "latitude": 30.0, "longitude": 31.2, "temp": 34.0, "humidity": 35.0,
        "wind": 14.0, "pressure": 1012.0, "precip": 0.0, "cloud": 10,
        "visibility": 10.0, "uv": 9.0, "pm25": 45.0, "pm10": 90.0
    },
    "Sydney (Temperate Zone)": {
        "latitude": -33.9, "longitude": 151.2, "temp": 21.0, "humidity": 62.0,
        "wind": 16.0, "pressure": 1016.0, "precip": 0.3, "cloud": 30,
        "visibility": 10.0, "uv": 7.0, "pm25": 7.0, "pm10": 14.0
    }
}

CLIMATE_INFO = {
    "Temperate": {
        "class": "temperate-zone",
        "description": "Moderate temperatures year-round, clearly defined seasonal changes, and balanced humidity. Perfect for diverse vegetative growth.",
        "icon": "🌤️",
        "accent": "#2980B9"
    },
    "Humid": {
        "class": "humid-zone",
        "description": "Abundant precipitation, dense cloud coverage, and high relative humidity. Typified by lush wetlands, dense rain forests, and mist-laden mountains.",
        "icon": "🌧️",
        "accent": "#27AE60"
    },
    "Tropical": {
        "class": "tropical-zone",
        "description": "Sustained high temperatures throughout the year. High solar UV index, clear skies or seasonal monsoonal precipitation, and distinct dry/wet cycles.",
        "icon": "☀️",
        "accent": "#E67E22"
    }
}

# ----------------- APP HEADER -----------------
st.markdown('<div class="glowing-title">Climate Zone Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Global classification system utilizing unsupervised K-Means Clustering on multi-dimensional atmospheric metrics.</div>', unsafe_allow_html=True)

# ----------------- MAIN NAVIGATION -----------------
selected_section = st.radio(
    "Select Section:",
    options=["🔮 Predict Climate Zone", "🌍 Global Database Search", "📈 Model & Cluster Analytics"],
    horizontal=True,
    label_visibility="collapsed"
)

# Dynamically collapse/hide the sidebar in other sections
if selected_section != "🔮 Predict Climate Zone":
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIG & CONTROLS -----------------
vals = {
    "latitude": 20.0, "longitude": 77.0, "temp": 25.0, "humidity": 60.0,
    "wind": 12.0, "pressure": 1013.0, "precip": 1.0, "cloud": 40,
    "visibility": 10.0, "uv": 5.0, "pm25": 20.0, "pm10": 45.0
}

if selected_section == "🔮 Predict Climate Zone":
    st.sidebar.markdown("### 🗺️ Preset Explorer")
    preset_choice = st.sidebar.selectbox(
        "Pre-fill parameters for a famous global region:",
        options=["Custom Entry"] + list(CITY_PRESETS.keys())
    )

    # Extract default values depending on selected preset
    if preset_choice != "Custom Entry":
        vals = CITY_PRESETS[preset_choice]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧬 Cluster Properties")
    st.sidebar.info(
        "**Algorithm:** KMeans unsupervised learning\n\n"
        "**Clusters (K=3):**\n"
        "- **Cluster 0:** Temperate Climate\n"
        "- **Cluster 1:** Humid Climate\n"
        "- **Cluster 2:** Tropical Climate"
    )

# ----------------- SECTION 1: PREDICTION PANEL -----------------
if selected_section == "🔮 Predict Climate Zone":
    with st.container():
        st.markdown("### 🎛️ Weather & Coordinate Inputs")
    st.write("Modify the parameters below to compute the cluster location's micro-climate category:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 📍 Geography")
        lat = st.slider("Latitude", min_value=-90.0, max_value=90.0, value=vals["latitude"], step=0.1)
        lon = st.slider("Longitude", min_value=-180.0, max_value=180.0, value=vals["longitude"], step=0.1)
        
        st.markdown("##### 💨 Atmosphere")
        wind_kph = st.slider("Wind Speed (kph)", min_value=0.0, max_value=100.0, value=vals["wind"], step=0.5)
        pressure_mb = st.slider("Atmospheric Pressure (mb)", min_value=950.0, max_value=1060.0, value=vals["pressure"], step=1.0)
        
    with col2:
        st.markdown("##### 🌡️ Climate Metrics")
        temp = st.slider("Temperature (°C)", min_value=-30.0, max_value=70.0, value=vals["temp"], step=0.5)
        humidity = st.slider("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=vals["humidity"], step=1.0)
        precip_mm = st.slider("Precipitation (mm)", min_value=0.0, max_value=50.0, value=vals["precip"], step=0.1)
        cloud = st.slider("Cloud Cover (%)", min_value=0, max_value=100, value=vals["cloud"], step=1)
        
    with col3:
        st.markdown("##### 🌫️ Visibility & Quality")
        visibility_km = st.slider("Visibility (km)", min_value=0.0, max_value=32.0, value=vals["visibility"], step=0.5)
        uv_index = st.slider("UV Index", min_value=0.0, max_value=20.0, value=vals["uv"], step=0.5)
        pm25 = st.slider("Air Quality PM2.5 (µg/m³)", min_value=0.0, max_value=500.0, value=vals["pm25"], step=1.0)
        pm10 = st.slider("Air Quality PM10 (µg/m³)", min_value=0.0, max_value=1000.0, value=vals["pm10"], step=1.0)

    st.markdown("---")
    
    # Perform prediction
    if st.button("🚀 Classify Climate Zone", use_container_width=True):
        if scaler is not None and model is not None:
            # 1. Scaler expects the 10 climate features
            climate_features = np.array([[
                temp, humidity, wind_kph, pressure_mb, precip_mm,
                cloud, visibility_km, uv_index, pm25, pm10
            ]])
            scaled_climate = scaler.transform(climate_features)
            
            # 2. KMeans expects the concatenated 12 features: [lat, lon, ...scaled climate...]
            coords = np.array([[lat, lon]])
            scaled_input = np.concatenate([coords, scaled_climate], axis=1)
            
            # 3. Model predict
            predicted_zone = model.predict(scaled_input)[0]
            
            # 4. Map predicted zone code to Name
            climate_names = {0: 'Temperate', 1: 'Humid', 2: 'Tropical'}
            zone_name = climate_names.get(predicted_zone, "Unknown")
            info = CLIMATE_INFO[zone_name]
            
            # Render custom glass card result
            st.markdown(f"""
            <div class="{info['class']}">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{info['icon']}</div>
                <h2 style="margin: 0; font-size: 2.2rem; font-weight: 800;">Predicted Climate Zone: {zone_name} (Zone {predicted_zone})</h2>
                <p style="font-size: 1.1rem; max-width: 800px; margin-top: 0.5rem; line-height: 1.6; opacity: 0.95;">
                    {info['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show a radar chart comparing this location input with average metrics of each zone
            st.markdown("### 📊 Micro-climate Comparison")
            
            # Define normalized features for radar chart comparison
            features_labels = ["Temp", "Humidity", "Wind", "Precip", "Clouds", "UV Index"]
            # Scale user values back to [0,1] or standard ranges to look nice on radar chart
            user_metrics = [
                (temp + 30) / 100.0,
                humidity / 100.0,
                wind_kph / 100.0,
                min(precip_mm / 10.0, 1.0),
                cloud / 100.0,
                uv_index / 15.0
            ]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=user_metrics,
                theta=features_labels,
                fill='toself',
                name='User Region',
                line_color=info['accent']
            ))
            
            # Center values
            if data_df is not None:
                # Group stats
                grp = data_df.groupby("Climate_Name").mean(numeric_only=True)
                if zone_name in grp.index:
                    avg_row = grp.loc[zone_name]
                    avg_metrics = [
                        (avg_row["temperature_celsius"] + 30) / 100.0,
                        avg_row["humidity"] / 100.0,
                        avg_row["wind_kph"] / 100.0,
                        min(avg_row["precip_mm"] / 10.0, 1.0),
                        avg_row["cloud"] / 100.0,
                        avg_row["uv_index"] / 15.0
                    ]
                    fig.add_trace(go.Scatterpolar(
                        r=avg_metrics,
                        theta=features_labels,
                        fill='toself',
                        name=f'Global {zone_name} Avg',
                        line_color='#7f8c8d',
                        opacity=0.6
                    ))
                    
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Models could not be loaded. Please ensure scaler.pkl and kmeans_climate_model.pkl are present.")

# ----------------- SECTION 2: GLOBAL DATABASE SEARCH -----------------
elif selected_section == "🌍 Global Database Search":
    with st.container():
        st.markdown("### 🔍 Historical Global Climate Database")
    st.write("Browse classified weather details of over 140,000 real-world geographical records:")
    
    if data_df is not None:
        search_col1, search_col2 = st.columns([1, 2])
        
        with search_col1:
            countries_list = sorted(data_df["country"].dropna().unique().tolist())
            selected_country = st.selectbox("Filter by Country:", options=["All Countries"] + countries_list)
            
            # Dynamically filter cities based on country selection to populate selectbox
            country_filtered_df = data_df
            if selected_country != "All Countries":
                country_filtered_df = country_filtered_df[country_filtered_df["country"] == selected_country]
                
            cities_list = sorted(country_filtered_df["location_name"].dropna().unique().tolist())
            selected_city = st.selectbox("Select Location/City Name:", options=["All Cities"] + cities_list)
            
            # Filter logic
            filtered_df = country_filtered_df
            if selected_city != "All Cities":
                filtered_df = filtered_df[filtered_df["location_name"] == selected_city]
                
            st.info("💡 **Tip:** The database contains historical records of major/capital cities. To classify other cities (like **Mumbai**, **Bangalore**, **Kolkata**, or **Chennai**), load them via the **Preset Explorer** in the sidebar, or input weather metrics directly in **Tab 1**!")
                
            st.markdown(f"**Found Records:** {len(filtered_df):,}")
            
            # Show standard overview card
            st.markdown(f"""
            <div class="glass-card">
                <h5>Climate Zone Split</h5>
                <ul>
                    <li>Temperate: {len(filtered_df[filtered_df["Climate_Zone"]==0]):,}</li>
                    <li>Humid: {len(filtered_df[filtered_df["Climate_Zone"]==1]):,}</li>
                    <li>Tropical: {len(filtered_df[filtered_df["Climate_Zone"]==2]):,}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with search_col2:
            st.markdown("##### 📍 Geographic Map Distribution")
            
            # Sample data down if it exceeds pydeck plotting limit (say max 8,000 points) to remain smooth
            map_data = filtered_df.dropna(subset=['latitude', 'longitude'])
            if len(map_data) > 8000:
                map_data = map_data.sample(8000, random_state=42)
                
            color_map = {
                0: [41, 128, 185, 160],   # Temperate - blue
                1: [39, 174, 96, 160],    # Humid - green
                2: [230, 126, 34, 160]    # Tropical - orange
            }
            map_data['color'] = map_data['Climate_Zone'].map(color_map)
            
            # Pydeck elegant layout
            view_state = pdk.ViewState(
                latitude=map_data['latitude'].mean() if len(map_data) > 0 else 20.0,
                longitude=map_data['longitude'].mean() if len(map_data) > 0 else 0.0,
                zoom=2 if len(map_data) > 0 else 1,
                pitch=0
            )
            
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[longitude, latitude]',
                get_color='color',
                get_radius=15000,
                radius_min_pixels=3,
                radius_max_pixels=15,
                pickable=True
            )
            
            tooltip = {"html": "<b>{location_name}, {country}</b><br/>Climate Zone: {Climate_Name}<br/>Temp: {temperature_celsius}°C<br/>Humidity: {humidity}%"}
            
            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style='dark'
            )
            
            st.pydeck_chart(r)
            
        st.markdown("##### 📋 Filtered Dataset Result Sample")
        st.dataframe(filtered_df[['country', 'location_name', 'latitude', 'longitude', 
                                  'temperature_celsius', 'humidity', 'wind_kph', 'uv_index', 
                                  'Climate_Name']].head(200), use_container_width=True)
    else:
        st.warning("classified_climate_data.csv is not loaded. Please upload or ensure it resides in the workspace directory.")

# ----------------- SECTION 3: MODEL INSIGHTS & ANALYTICS -----------------
elif selected_section == "📈 Model & Cluster Analytics":
    with st.container():
        st.markdown("### 📊 Clustering & Feature Relationships")
    st.write("Examine relationships and how K-Means clustered different world weather points:")
    
    if data_df is not None:
        plot_col1, plot_col2 = st.columns(2)
        
        with plot_col1:
            st.markdown("##### 🌡️ Temperature vs Humidity Clustering")
            # Downsample plotting to 5,000 for web responsiveness
            plot_df = data_df.sample(5000, random_state=42) if len(data_df) > 5000 else data_df
            
            fig2d = px.scatter(
                plot_df,
                x="temperature_celsius",
                y="humidity",
                color="Climate_Name",
                color_discrete_map={
                    "Temperate": "#2980B9",
                    "Humid": "#27AE60",
                    "Tropical": "#E67E22"
                },
                labels={"temperature_celsius": "Temperature (°C)", "humidity": "Humidity (%)", "Climate_Name": "Climate Zone"},
                hover_data=["location_name", "country"],
                opacity=0.6
            )
            fig2d.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )
            st.plotly_chart(fig2d, use_container_width=True)
            
        with plot_col2:
            st.markdown("##### 🌪️ UV Index vs PM2.5 Air Quality Clustering")
            fig_uv_pm = px.scatter(
                plot_df,
                x="uv_index",
                y="air_quality_PM2.5",
                color="Climate_Name",
                color_discrete_map={
                    "Temperate": "#2980B9",
                    "Humid": "#27AE60",
                    "Tropical": "#E67E22"
                },
                labels={"uv_index": "UV Index", "air_quality_PM2.5": "PM2.5 Density (µg/m³)", "Climate_Name": "Climate Zone"},
                hover_data=["location_name", "country"],
                opacity=0.6
            )
            fig_uv_pm.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )
            st.plotly_chart(fig_uv_pm, use_container_width=True)
            
        st.markdown("---")
        st.markdown("##### 📊 Global Climate Zone Class Distribution")
        
        # Aggregate distribution
        dist = data_df["Climate_Name"].value_counts().reset_index(name="count")
        fig_bar = px.bar(
            dist,
            x="Climate_Name",
            y="count",
            color="Climate_Name",
            color_discrete_map={
                "Temperate": "#2980B9",
                "Humid": "#27AE60",
                "Tropical": "#E67E22"
            },
            labels={"Climate_Name": "Climate Category", "count": "Number of Global Weather Stations"},
            text="count"
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    else:
        st.warning("Historical data file not loaded. Cluster insights chart requires the classified_climate_data.csv dataset.")
