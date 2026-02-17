import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="MacroSentinel", page_icon="🎯", layout="wide")

PORTFOLIO = {
    'Rare Earth Metals': {'weight': 25, 'change_1d': 2.1, 'change_1m': 8.5, 'ytd': 15.2},
    'Essential Metals': {'weight': 22, 'change_1d': 0.8, 'change_1m': 5.2, 'ytd': 8.7},
    'European Banks': {'weight': 20, 'change_1d': -0.5, 'change_1m': 2.1, 'ytd': 4.2},
    'China': {'weight': 18, 'change_1d': 2.1, 'change_1m': -3.2, 'ytd': 8.5},
    'European Defense': {'weight': 15, 'change_1d': 4.2, 'change_1m': 12.5, 'ytd': 22.1}
}

perf_ytd = sum(d['ytd'] * d['weight']/100 for d in PORTFOLIO.values())
perf_1d = sum(d['change_1d'] * d['weight']/100 for d in PORTFOLIO.values())
perf_1m = sum(d['change_1m'] * d['weight']/100 for d in PORTFOLIO.values())

st.title("🎯 MacroSentinel Dashboard")
st.write(f"Update: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

col1, col2, col3 = st.columns(3)
col1.metric("1 Tag", f"{perf_1d:+.2f}%")
col2.metric("1 Monat", f"{perf_1m:+.2f}%")
col3.metric("YTD 2025", f"{perf_ytd:+.2f}%")

st.subheader("Portfolio")
df = pd.DataFrame([
    {'Asset': a, 'Gewicht': f"{d['weight']}%", 'YTD': f"{d['ytd']:+.1f}%"}
    for a, d in PORTFOLIO.items()
])
st.dataframe(df, use_container_width=True)

fig = px.pie(values=[d['weight'] for d in PORTFOLIO.values()], 
             names=list(PORTFOLIO.keys()))
st.plotly_chart(fig)

if st.button("📧 E-Mail senden"):
    try:
        EMAIL = "in2dblu@gmail.com"
        PASSWORT = "wyjnsorizdmbsknu"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'MacroSentinel - {datetime.now().strftime("%d.%m.%Y")}'
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        html = f"<html><body><h1>Portfolio: {perf_ytd:+.2f}%</h1></body></html>"
        msg.attach(MIMEText(html, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORT)
        server.send_message(msg)
        server.quit()
        st.success("✅ E-Mail gesendet!")
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
