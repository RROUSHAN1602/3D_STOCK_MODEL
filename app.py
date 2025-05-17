import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import pyotp
from SmartApi.smartConnect import SmartConnect
import plotly.graph_objects as go

# Config
st.set_page_config(page_title="📈 3D Money Flow Dashboard", layout="wide")
st.title("📊 Advanced Stock Dashboard – Volume | Price | Money Flow")

# Angel One Login
api_key = st.secrets["API_KEY"]
client_id = st.secrets["CLIENT_ID"]
password = st.secrets["PASSWORD"]
totp_secret = st.secrets["TOTP_SECRET"]

try:
    totp = pyotp.TOTP(totp_secret).now()
    obj = SmartConnect(api_key=api_key)
    session_data = obj.generateSession(client_id, password, totp)
    st.success("✅ Angel One Login Successful")
except Exception as e:
    st.error(f"❌ Login Failed: {e}")
    st.stop()

# Stock list (add tokens as needed)
stock_list = {
    "RELIANCE": "2885",
    "POLYCAB": "9590",
    "TCS": "11536",
    "INFY": "1594",
    # ...
}

# UI
stock_name = st.selectbox("📌 Select Stock", list(stock_list.keys()))
interval = st.selectbox("🕒 Select Interval", ["ONE_MINUTE","FIVE_MINUTE","FIFTEEN_MINUTE","THIRTY_MINUTE","ONE_HOUR","ONE_DAY"])
from_date = st.date_input("📆 From Date", dt.date.today() - dt.timedelta(days=5))
to_date = st.date_input("📆 To Date", dt.date.today())
if from_date > to_date:
    st.warning("⚠️ 'From Date' cannot be after 'To Date'")
    st.stop()

# Fetch OHLC
def fetch_ohlc_data(symbol, interval, from_date, to_date):
    try:
        params = {
            "exchange":"NSE",
            "symboltoken":stock_list[symbol],
            "interval":interval,
            "fromdate":f"{from_date} 09:15",
            "todate":f"{to_date} 15:30"
        }
        response = obj.getCandleData(params)
        if not response.get("status") or "data" not in response:
            return None
        df = pd.DataFrame(response["data"], columns=["timestamp","open","high","low","close","volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        for col in ["open","high","low","close","volume"]:
            df[col] = df[col].astype(float)
        return df
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        return None

df = fetch_ohlc_data(stock_name, interval, from_date, to_date)
if df is None or df.empty:
    st.warning("⚠️ No data available.")
    st.stop()

# CMF Calculation
def calculate_cmf(df, period=20):
    mf = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (df["high"] - df["low"])
    mf = mf.replace([np.inf, -np.inf], 0).fillna(0)
    mf_vol = mf * df["volume"]
    df["cmf"] = mf_vol.rolling(window=period).sum() / df["volume"].rolling(window=period).sum()
    return df.dropna()

df = calculate_cmf(df)

# Divergence
df["divergence"] = df["cmf"].diff() * df["close"].diff() < 0

# Plots
def plot_3d(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=df["volume"], y=df["close"], z=df["cmf"],
                               mode="markers+lines",
                               marker=dict(size=4, color=df["cmf"], colorscale="Viridis")))
    fig.update_layout(scene=dict(xaxis_title="Volume", yaxis_title="Price", zaxis_title="CMF"),
                      margin=dict(l=0, r=0, b=0, t=30), height=700)
    return fig

def plot_2d(x, y, title):
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers"))
    fig.update_layout(title=title, xaxis_title=x.name, yaxis_title=y.name)
    return fig

tab1, tab2, tab3, tab4 = st.tabs(["3D Chart","Price vs CMF","Volume vs CMF","Divergence"])
with tab1:
    st.plotly_chart(plot_3d(df), use_container_width=True)
with tab2:
    st.plotly_chart(plot_2d(df["timestamp"], df["close"], "Price vs CMF"), use_container_width=True)
with tab3:
    st.plotly_chart(plot_2d(df["timestamp"], df["volume"], "Volume vs CMF"), use_container_width=True)
with tab4:
    st.write("🔴 Divergence points")
    colors = np.where(df["divergence"], "red", "blue")
    fig = go.Figure(go.Scatter(x=df["timestamp"], y=df["close"], mode="markers", marker=dict(color=colors)))
    st.plotly_chart(fig, use_container_width=True)
