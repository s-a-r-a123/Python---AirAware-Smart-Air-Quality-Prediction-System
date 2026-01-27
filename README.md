# 🌍 Air Aware – Smart Air Quality Monitoring System

Air pollution is a growing public health concern, yet most people lack access to clear, actionable, and understandable air quality information. **Air Aware** is a smart air quality monitoring and visualization system designed to help users understand pollution levels, track trends, and make informed health decisions.



## 🚨 Problem Statement

  Air pollution is a growing concern in urban environments, directly impacting
human health and environmental quality. Accurate forecasting of air quality
can help authorities take preventive measures, issue warnings, and inform the
public. 

  This project aims to build a time series forecasting system that predicts air
quality index (AQI) and pollutant levels using historical pollution data. The goal
is to empower environmental agencies, city planners, and the public with
timely insights for healthier decision-making.

---

## 🎯 Objective

The objectives of this project are:
- To monitor air quality using pollution data
- To visualize PM2.5 and PM10 trends
- To analyze historical air quality patterns
- To forecast future pollution levels
- To spread awareness about environmental and health risks



## 💡 Proposed Solution

Air Aware provides a centralized and user-friendly dashboard that:
1. Ingests air quality data
2. Cleans and preprocesses pollutant values
3. Analyzes AQI-related indicators
4. Visualizes historical trends
5. Predicts short-term pollution levels
6. Displays insights using an interactive dashboard

---

## ✨ Key Features

-  Interactive air quality dashboard
-  PM2.5 and PM10 trend visualization
-  Pollution level forecasting
-  Clean and intuitive UI
-  Uses sample/dummy air quality data
-  Easy local setup



## 🛠 Tech Stack

- **Language:** Python  
- **Framework:** Streamlit  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Plotly  
- **Forecasting:** Scikit-learn 

---

## 📂 Project Structure

  air-aware/                                                                                                                                           
  ├── Dashboard.py                                                                                                                                    
  ├── requirements.txt           
  ├── README.md                                                                                                                                       
  ├── data/                                                                                                                                           
  │   └── air_dataset.csv                                                                                                                         
  ├── assets/                                                                                                                                         
      └── screenshots                                                                                                                                 

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip installed

### Steps to Run Locally

```bash
  - git clone https://github.com/s-a-r-a123/Python---AirAware-Smart-Air-Quality-Prediction-System.git
  - cd Python---AirAware-Smart-Air-Quality-Prediction-System
  - pip install -r requirements.txt
  - python Dashboard.py
```

### The application will start on:
  - http://localhost:8501

---

## Dataset Info
  The project uses a CSV dataset air_dataset.csv containing air quality measurements.
This dataset is included for demonstration purposes and can be replaced or expanded with real-time API data in future versions.

---

## Contact
  If you have questions or want help improving this project, open an issue or drop a message! ( •̀ ω •́ )✧
