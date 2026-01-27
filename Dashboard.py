%%writefile app.py
import streamlit as st
import plotly.graph_objects as go
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Smart Air Quality Dashboard", layout="wide")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False
if "admin_loaded" not in st.session_state:
    st.session_state.admin_loaded = False

# --------------------------------------------------
# YOUR EARTH LOADER (UNCHANGED)
# --------------------------------------------------
def show_earth_loader(seconds=2, text="Connecting…"):
    loader = st.empty()
    loader.markdown(f"""
    <style>
    .loader-wrapper {{
      position: fixed; inset: 0; z-index: 9999;
      display: flex; justify-content: center; align-items: center;
      background: radial-gradient(circle at top,#0f172a,#020617);
    }}
    .earth {{ display: flex; flex-direction: column; align-items: center; gap: 1rem; }}
    .earth p {{ color: white; font-size: 1.1rem; letter-spacing: 1px; }}
    .earth-loader {{
      --watercolor:#3f51d9; --landcolor:#9be24f;
      width:8em; height:8em; position:relative; overflow:hidden;
      border-radius:50%; border:2px solid rgba(255,255,255,0.9);
      background: radial-gradient(circle at 30% 30%,#6a78ff,var(--watercolor));
      box-shadow: inset 0.45em 0.45em rgba(255,255,255,.22),
                  inset -0.6em -0.6em rgba(0,0,0,.42),
                  0 0 22px rgba(79,112,255,.4);
    }}
    .earth-loader svg {{ position:absolute; width:8.2em; opacity:.9; }}
    .earth-loader svg:nth-child(1) {{ top:-2.6em; animation:round1 4s infinite linear; }}
    .earth-loader svg:nth-child(2) {{ bottom:-2.8em; animation:round2 4s infinite linear .9s; }}
    .earth-loader svg:nth-child(3) {{ top:-1.8em; animation:round1 4s infinite linear 1.8s; }}

    @keyframes round1 {{
      0% {{ left:-3.5em; opacity:1; }}
      50% {{ left:-8em; opacity:0; }}
      100% {{ left:-3.5em; opacity:1; }}
    }}
    @keyframes round2 {{
      0% {{ left:5.5em; opacity:1; }}
      50% {{ left:-9em; opacity:0; }}
      100% {{ left:5.5em; opacity:1; }}
    }}
    </style>

    <div class="loader-wrapper">
      <div class="earth">
        <div class="earth-loader">
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 35 C138 38,162 68,158 105 C154 142,120 160,100 156
               C62 152,38 125,42 100 C46 70,70 40,100 35Z"/></svg>
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 45 C132 48,152 78,148 108 C144 138,118 148,100 145
               C68 142,48 120,52 100 C56 78,72 50,100 45Z"/></svg>
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 40 C130 44,150 72,146 104 C142 136,118 148,100 144
               C70 140,50 118,54 100 C58 74,74 46,100 40Z"/></svg>
        </div>
        <p>{text}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(seconds)
    loader.empty()


st.title("🌍 Air Aware")


# --------------------------------------------------
# STARTUP LOADER
# --------------------------------------------------
if not st.session_state.loaded:
    show_earth_loader(2, "Initializing Air Quality System…")
    st.session_state.loaded = True
    st.rerun()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("Controls")
st.sidebar.selectbox("Monitoring Station", ["Downtown","Suburb","Industrial Area"])
st.sidebar.selectbox("Time Range", ["Last 24 Hours","Last Week"])
admin_mode = st.sidebar.toggle("Admin Mode")

# --------------------------------------------------
# ADMIN MODE
# --------------------------------------------------
if admin_mode and not st.session_state.admin_loaded:
    show_earth_loader(2, "Entering Admin Mode…")
    st.session_state.admin_loaded = True
    st.rerun()

if admin_mode:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Admin Panel")
    uploaded = st.sidebar.file_uploader("Upload AQI Dataset", type=["csv"])
    threshold = st.sidebar.slider("Alert Threshold (AQI)", 50, 300, 150)

    if st.sidebar.button("📊 Refresh Model"):
        show_earth_loader(2, "Refreshing AI Model…")
        st.sidebar.success("Model Updated Successfully")

    if uploaded:
        show_earth_loader(2, "Uploading Dataset…")
        st.sidebar.success("Dataset Uploaded")

# --------------------------------------------------
# AQI + FORECAST (TOP ROW)
# --------------------------------------------------
aqi = 70
col1, col2 = st.columns([1.2,1])

with col1:
    st.subheader("Current Air Quality")

    fig = go.Figure(go.Pie(
      values=[50,50,50,50,50],
      hole=0.75,
      rotation=90,
      marker=dict(colors=["#16a34a","#eab308","#f97316","#dc2626","#7c3aed"]),
      textinfo="none"
    ))


    fig.add_trace(go.Pie(
        values=[aqi, 250 - aqi],
        hole=0.75,
        rotation=90,
        marker=dict(colors=["rgba(0,0,0,0)", "rgba(15,23,42,0.85)"]),
        textinfo="none",
        showlegend=False
    ))

    fig.add_annotation(
        text=f"<b>{aqi}</b><br>AQI<br><span style='color:#facc15'>Moderate</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=24)   # optional: slightly larger center text
    )

    fig.update_layout(
        height=250,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Forecast")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=[40,38,45,52,48,44],
        mode="lines+markers",
        name="Historical",
        line=dict(color="#38bdf8", width=3)
    ))

    fig.add_trace(go.Scatter(
        y=[44,42,36,42,48],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#a855f7", width=3, dash="dot")
    ))

    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# POLLUTANT TRENDS
# --------------------------------------------------
st.subheader("Pollutant Trends")
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=days, y=[45,48,46,55,60,52,50],
    name="PM2.5",
    line=dict(color="#38bdf8", width=3)
))

fig.add_trace(go.Scatter(
    x=days, y=[30,32,31,38,40,35,33],
    name="NO2",
    line=dict(color="#facc15", width=3)
))

fig.add_trace(go.Scatter(
    x=days, y=[25,27,28,30,32,30,29],
    name="O3",
    line=dict(color="#22c55e", width=3)
))

fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# DAILY ALERTS
# --------------------------------------------------
st.subheader("Daily Air Quality Alerts")
c1,c2,c3 = st.columns(3)
c1.success("☀️ Morning!\nGood air quality\nSafe for outdoor exercise")
c2.warning("🌤 Afternoon!\nModerate AQI\nSensitive groups take care")
c3.error("🌙 Night!\nPoor ventilation\nAvoid prolonged outdoor stay")

st.markdown("<hr><center>Smart Air Quality Dashboard 🌍</center>",
            unsafe_allow_html=True)
