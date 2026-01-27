%%writefile app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide", page_icon="🌍")

# Custom CSS with animations
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {
        width: 100%;
        background-color: #4e73df;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2e59d9;
        transform: scale(1.05);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .pulse-emoji {
        animation: pulse 2s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .bounce-emoji {
        animation: bounce 1.5s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .rotate-emoji {
        animation: rotate 3s linear infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .shake-emoji {
        animation: shake 0.5s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    .weather-header {
        font-size: 2.5em;
        text-align: center;
        margin: 20px 0;
    }
    
    .alert-box {
        animation: fadeIn 0.5s ease-out;
        margin: 10px 0;
        padding: 15px;
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    
    .alert-box:hover {
        transform: translateX(10px);
    }
    
    .metric-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .loading-spinner {
        animation: rotate 1s linear infinite;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Animated Header
st.markdown("""
    <div class="weather-header fade-in">
        <span class="pulse-emoji">🌍</span> Air Quality Dashboard <span class="pulse-emoji">💨</span>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls with animated emojis
st.sidebar.markdown('<h2><span class="bounce-emoji">🎛️</span> Controls</h2>', unsafe_allow_html=True)

st.sidebar.markdown('<p><span class="pulse-emoji">📍</span> <b>Monitoring Station</b></p>', unsafe_allow_html=True)
monitoring_station = st.sidebar.selectbox(
    "Monitoring Station",
    ["Downtown 🏙️", "Suburb 🏘️", "Industrial Area 🏭", "Park 🌳"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<p><span class="pulse-emoji">⏰</span> <b>Time Range</b></p>', unsafe_allow_html=True)
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 24 Hours ⏱️", "Last 48 Hours 📅", "Last Week 🗓️"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<p><span class="pulse-emoji">🧪</span> <b>Pollutant</b></p>', unsafe_allow_html=True)
pollutant = st.sidebar.selectbox(
    "Pollutant",
    ["PM2.5 🔬", "PM10 💨", "NO2 🚗", "O3 ☀️", "CO 🏭"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<p><span class="pulse-emoji">🔮</span> <b>Forecast Horizon</b></p>', unsafe_allow_html=True)
forecast_horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    ["24 Hours 📊", "48 Hours 📈", "72 Hours 📉"],
    label_visibility="collapsed"
)

# Animated update button
if st.sidebar.button("🔄 Update Dashboard"):
    with st.spinner(''):
        st.sidebar.markdown('<div class="loading-spinner">⏳</div>', unsafe_allow_html=True)
        time.sleep(1)
        st.sidebar.success("✅ Dashboard Updated!")
        st.rerun()

st.sidebar.markdown("---")
admin_mode = st.sidebar.checkbox("🔐 Admin Mode")

if admin_mode:
    st.sidebar.markdown('<span class="shake-emoji">⚠️</span> Admin Mode Active', unsafe_allow_html=True)

# Quick Stats Row
st.markdown("### 📊 Quick Stats")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
        <div class="metric-container fade-in">
            <div class="pulse-emoji">🌡️</div>
            <h3>Temperature</h3>
            <h2>24°C</h2>
        </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
        <div class="metric-container fade-in">
            <div class="pulse-emoji">💧</div>
            <h3>Humidity</h3>
            <h2>65%</h2>
        </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
        <div class="metric-container fade-in">
            <div class="rotate-emoji">🌪️</div>
            <h3>Wind Speed</h3>
            <h2>12 km/h</h2>
        </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown("""
        <div class="metric-container fade-in">
            <div class="bounce-emoji">☁️</div>
            <h3>Visibility</h3>
            <h2>8 km</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content
col1, col2 = st.columns([1, 1])

# Current Air Quality Gauge
with col1:
    st.markdown('<h3><span class="pulse-emoji">🎯</span> Current Air Quality</h3>', unsafe_allow_html=True)
    
    # Create gauge chart
    current_aqi = 68
    
    # AQI status emoji
    if current_aqi <= 50:
        status_emoji = "😊"
        status_text = "Good"
        status_color = "#00e400"
    elif current_aqi <= 100:
        status_emoji = "😐"
        status_text = "Moderate"
        status_color = "#ffff00"
    elif current_aqi <= 150:
        status_emoji = "😷"
        status_text = "Unhealthy for Sensitive"
        status_color = "#ff7e00"
    elif current_aqi <= 200:
        status_emoji = "😨"
        status_text = "Unhealthy"
        status_color = "#ff0000"
    else:
        status_emoji = "☠️"
        status_text = "Hazardous"
        status_color = "#8f3f97"
    
    st.markdown(f"""
        <div style="text-align: center; font-size: 3em;" class="pulse-emoji">
            {status_emoji}
        </div>
    """, unsafe_allow_html=True)
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_aqi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"AQI<br><span style='font-size:0.8em;color:{status_color}'>{status_text}</span>", 
                 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "white", 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#00e400'},
                {'range': [50, 100], 'color': '#ffff00'},
                {'range': [100, 150], 'color': '#ff7e00'},
                {'range': [150, 200], 'color': '#ff0000'},
                {'range': [200, 300], 'color': '#8f3f97'},
                {'range': [300, 500], 'color': '#7e0023'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': current_aqi
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)

# PM2.5 Forecast
with col2:
    st.markdown('<h3><span class="bounce-emoji">📈</span> PM2.5 Forecast</h3>', unsafe_allow_html=True)
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=24, freq='H')
    historical = [35, 32, 38, 42, 45, 48, 52, 50]
    forecast = [48, 52, 45, 42, 38, 35, 32, 30, 28, 32, 35, 38, 42, 45, 40, 35]
    
    fig_forecast = go.Figure()
    
    # Historical line
    fig_forecast.add_trace(go.Scatter(
        x=list(range(len(historical))),
        y=historical,
        mode='lines+markers',
        name='📊 Historical',
        line=dict(color='#4e73df', width=3),
        marker=dict(size=6)
    ))
    
    # Forecast line
    fig_forecast.add_trace(go.Scatter(
        x=list(range(len(historical)-1, len(historical)+len(forecast))),
        y=[historical[-1]] + forecast,
        mode='lines+markers',
        name='🔮 Forecast',
        line=dict(color='#ff7e00', width=3, dash='dot'),
        marker=dict(size=6)
    ))
    
    fig_forecast.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis_title="Time ⏰",
        yaxis_title="PM2.5 (μg/m³)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)

st.markdown("---")

# Bottom section
col3, col4 = st.columns([1, 1])

# Pollutant Trends
with col3:
    st.markdown('<h3><span class="rotate-emoji">📉</span> Pollutant Trends</h3>', unsafe_allow_html=True)
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    pm25_values = [42, 38, 35, 40, 45, 42, 38]
    no2_values = [35, 32, 30, 38, 42, 38, 35]
    o3_values = [28, 30, 32, 35, 38, 35, 32]
    
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=days, y=pm25_values,
        mode='lines+markers',
        name='🔬 PM2.5',
        line=dict(color='#4e73df', width=2),
        marker=dict(size=8)
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=days, y=no2_values,
        mode='lines+markers',
        name='🚗 NO2',
        line=dict(color='#1cc88a', width=2),
        marker=dict(size=8)
    ))
    
    fig_trends.add_trace(go.Scatter(
        x=days, y=o3_values,
        mode='lines+markers',
        name='☀️ O3',
        line=dict(color='#e74a3b', width=2),
        marker=dict(size=8)
    ))
    
    fig_trends.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis_title="",
        yaxis_title="Concentration (μg/m³)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

# Alert Notifications
with col4:
    st.markdown('<h3><span class="shake-emoji">🔔</span> Alert Notifications</h3>', unsafe_allow_html=True)
    
    # Alert 1
    st.markdown("""
        <div class="alert-box" style="background-color: #fff3cd; border-left: 5px solid #ffc107;">
            <span class="pulse-emoji" style="font-size: 1.5em;">⚠️</span>
            <strong>Moderate air quality expected</strong><br>
            <small>📅 Tomorrow, 10:00 AM</small>
        </div>
    """, unsafe_allow_html=True)
    
    # Alert 2
    st.markdown("""
        <div class="alert-box" style="background-color: #d4edda; border-left: 5px solid #28a745;">
            <span class="bounce-emoji" style="font-size: 1.5em;">✅</span>
            <strong>Good air quality today</strong><br>
            <small>📅 Today, 8:00 AM</small>
        </div>
    """, unsafe_allow_html=True)
    
    # Alert 3
    st.markdown("""
        <div class="alert-box" style="background-color: #d1ecf1; border-left: 5px solid #17a2b8;">
            <span class="rotate-emoji" style="font-size: 1.5em;">🔄</span>
            <strong>Model update completed</strong><br>
            <small>📅 Yesterday, 11:30 PM</small>
        </div>
    """, unsafe_allow_html=True)
    
    # Alert 4 - New
    st.markdown("""
        <div class="alert-box" style="background-color: #f8d7da; border-left: 5px solid #dc3545;">
            <span class="shake-emoji" style="font-size: 1.5em;">🚨</span>
            <strong>High pollution alert</strong><br>
            <small>📅 2 days ago, 3:00 PM</small>
        </div>
    """, unsafe_allow_html=True)

# Footer with animated icons
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <span class="pulse-emoji">🌱</span>
        <span class="bounce-emoji">💚</span>
        <span class="pulse-emoji">🌍</span>
        <br>
        <p style="color: #666; margin-top: 10px;">
            Real-time Air Quality Monitoring System | Last Updated: <span class="rotate-emoji">🔄</span> Just now
        </p>
    </div>
""", unsafe_allow_html=True)

# Floating action button animation
st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 999;">
        <div class="bounce-emoji" style="font-size: 3em; cursor: pointer; 
             background: white; border-radius: 50%; padding: 10px; 
             box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            💬
        </div>
    </div>
""", unsafe_allow_html=True)
