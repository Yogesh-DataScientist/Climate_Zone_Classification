🌍 Climate Zone Classification using K-Means Clustering

An interactive Machine Learning project that classifies global regions into different climate zones using the K-Means Clustering algorithm and visualizes climate patterns through a modern Streamlit dashboard.

📌 Project Overview

Climate classification is important for environmental monitoring, agriculture planning, weather forecasting, and climate analysis. Traditional climate classification methods are often manual and difficult to apply to large-scale datasets.

This project uses Unsupervised Machine Learning to automatically group regions with similar weather characteristics into meaningful climate zones such as:

Temperate
Humid
Tropical

The system is built using a large-scale global weather dataset containing over 143,000+ climate records and multiple atmospheric parameters.

🚀 Features

✅ Climate Zone Classification using K-Means Clustering
✅ Interactive Streamlit Dashboard
✅ Real-Time Climate Prediction
✅ Global Climate Database Search
✅ Pydeck World Map Visualization
✅ Radar Chart Climate Comparison
✅ Climate Analytics Dashboard
✅ Dark Theme Glassmorphism UI
✅ Model Persistence using Pickle Files
✅ Silhouette Score Evaluation

🧠 Machine Learning Workflow
Dataset Collection
        ↓
Data Preprocessing
        ↓
Feature Selection
        ↓
Feature Scaling
        ↓
Elbow Method
        ↓
K-Means Clustering
        ↓
Climate Zone Classification
        ↓
Cluster Evaluation
        ↓
Streamlit Deployment
📂 Dataset Information
Dataset Size: 143,847 Rows
Total Columns: 41
Source: Global Weather Repository Dataset
Selected Features
Feature	Description
temperature_celsius	Temperature
humidity	Humidity Level
wind_kph	Wind Speed
pressure_mb	Atmospheric Pressure
precip_mm	Rainfall
cloud	Cloud Coverage
visibility_km	Visibility
uv_index	UV Index
air_quality_PM2.5	PM2.5 Pollution
air_quality_PM10	PM10 Pollution
latitude	Geographical Coordinate
longitude	Geographical Coordinate
⚙️ Technologies Used
Technology	Purpose
Python	Core Programming
Streamlit	Web Application
Scikit-learn	Machine Learning
Pandas	Data Processing
NumPy	Numerical Computing
Matplotlib	Visualization
Seaborn	Statistical Graphs
Plotly	Interactive Charts
Pydeck	Geospatial Mapping
📊 Model Details
Algorithm Used
K-Means Clustering
Optimal Clusters
K = 3
Climate Categories
Cluster	Climate Zone
0	Temperate
1	Humid
2	Tropical
Evaluation Metric
Silhouette Score: 0.56
💻 Streamlit Application Modules
🔹 Predict Climate Zone
User input climate parameters
Real-time climate prediction
Interactive radar chart comparison
🔹 Global Database Explorer
Country & city filtering
Climate search system
Interactive Pydeck map visualization
🔹 Model Analytics Dashboard
Scatter plot visualizations
Cluster analysis
Climate distribution charts
📁 Project Structure
Climate-Zone-Classification/
│
├── app.py
├── classified_climate_data.csv
├── kmeans_climate_model.pkl
├── scaler.pkl
├── requirements.txt
├── README.md
└── images/
▶️ Installation & Execution
Clone Repository
git clone https://github.com/your-username/climate-zone-classification.git
Install Dependencies
pip install -r requirements.txt
Run Streamlit App
streamlit run app.py
📈 Visualizations Included
Climate Distribution Charts
Scatter Plots
Correlation Heatmaps
Radar Charts
Interactive World Map
Cluster Analytics
🔮 Future Enhancements
Real-time Weather API Integration
Satellite Data Analysis
Deep Learning-based Climate Prediction
GIS Integration
Real-time Monitoring Dashboard
Mobile Responsive Deployment
📚 Applications
Environmental Monitoring
Agriculture Planning
Climate Research
Disaster Management
Smart City Planning
Weather Pattern Analysis
👨‍💻 Author

Yogeshwaran S

⭐ Conclusion

This project demonstrates how Unsupervised Machine Learning can effectively classify and analyze global climate patterns using real-world weather data. By combining K-Means clustering with an interactive Streamlit dashboard, the system provides an intelligent and scalable climate analysis platform with meaningful visual insights.
