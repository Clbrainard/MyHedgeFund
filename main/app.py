import streamlit as st
import re
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="MyHedgeFund", layout="wide")

# Sidebar Navigation with larger text
st.sidebar.title("## Navigation")
st.sidebar.markdown("---")

pages = {
    "📊 **Dashboard**": "Dashboard",
    "📈 **Trades**": "Trades",
    "💼 **Positions**": "Positions",
    "🏆 **Leaderboard**": "Leaderboard",
    "⚙️ **Options Simulator**": "Options Simulator",
    "📊 **Position Simulator**": "Position Simulator",
    "🔧 **Settings**": "Settings"
}

page = st.sidebar.radio("### Select a Page", list(pages.keys()))
page = pages[page]

# Dashboard Page
if page == "Dashboard":
    st.title("MyHedgeFund - Dashboard")
    
    # Portfolio Performance Metrics
    st.subheader("Portfolio Performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total P/L", "$5,000", "+10%")
    col2.metric("Total Gain", "$7,500", "12%")
    col3.metric("Portfolio Value", "$55,000")
    col4.metric("Total Positions", "3")
    
    # Candlestick chart with line graph overlay
    st.subheader("Market Overview")
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        open=[100, 102, 101, 105, 107],
        high=[110, 112, 108, 115, 118],
        low=[95, 98, 97, 100, 105],
        close=[105, 107, 103, 110, 115],
        name="Fund Performance"
    ))
    
    fig.add_trace(go.Scatter(
        x=["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        y=[103, 105, 104, 108, 110],
        mode="lines",
        name="SPY Index",
        line=dict(color="blue")
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Metrics Tile
    st.subheader("Detailed Portfolio Metrics")
    st.write("(More in-depth analytics coming soon)")

# Positions Page
elif page == "Positions":
    st.title("Positions")
    st.write("### Active Positions")
    
    # Example position data
    positions = [
        {"Ticker": "AAPL", "P/L": "$1,500", "Gain": "5%", "Size": "$10,000"},
        {"Ticker": "TSLA", "P/L": "$2,000", "Gain": "8%", "Size": "$15,000"},
        {"Ticker": "AMZN", "P/L": "$1,500", "Gain": "7%", "Size": "$12,000"}
    ]
    
    for pos in positions:
        with st.container():
            st.subheader(f"{pos['Ticker']} - {pos['P/L']} ({pos['Gain']})")
            col1, col2, col3 = st.columns(3)
            col1.metric("P/L", pos['P/L'])
            col2.metric("Gain", pos['Gain'])
            col3.metric("Position Size", pos['Size'])
            
            # Example trades for each position
            trade_data = pd.DataFrame({
                "Trade Type": ["Buy", "Buy", "Sell"],
                "Quantity": [50, 30, 20],
                "Price": [150.0, 160.0, 170.0],
                "Date": ["2024-01-10", "2024-02-05", "2024-02-20"]
            })
            st.table(trade_data)
            
            # Option to add options table
            if st.checkbox(f"Show Options for {pos['Ticker']}"):
                options_data = pd.DataFrame({
                    "Type": ["Call", "Put"],
                    "Strike": [155.0, 145.0],
                    "Expiry": ["2024-06-21", "2024-06-21"],
                    "Premium": [5.2, 4.3]
                })
                st.table(options_data)

# Trades Page
elif page == "Trades":
    st.title("Trades")
    st.write("### Add a new trade")
    
    trade_type = st.selectbox("Select Trade Type", ["Stock", "Option"], key="trade_type")
    
    def validate_ticker_input(ticker):
        return re.sub(r'[^A-Z]', '', ticker.upper())
    
    ticker = st.text_input("Ticker Symbol", key="ticker")
    ticker = validate_ticker_input(ticker)
    
    st.number_input("Price", step=0.01, key="price")
    st.number_input("Quantity", step=1, key="quantity")
    trade_action = st.selectbox("Trade Type", ["Long", "Sell", "Short", "Cover"], key="trade_action")
    
    if trade_type == "Option":
        st.number_input("Strike Price", step=0.01, key="strike")
        expiry_date = st.date_input("Expiry Date", key="expiry")
        put_call = st.selectbox("Put/Call", ["Put", "Call"], key="put_call")
    
    st.button("Submit Trade")

# Leaderboard Page
elif page == "Leaderboard":
    st.title("Leaderboard")
    st.write("### Top Performers")
    st.write("(Leaderboard functionality coming soon)")

# Options Simulator Page
elif page == "Options Simulator":
    st.title("Options Simulator")
    st.write("### Simulate different option strategies")
    st.write("(Simulation tools coming soon)")

# Position Simulator Page
elif page == "Position Simulator":
    st.title("Position Simulator")
    st.write("### Experiment with different portfolio allocations")
    st.write("(Simulation tools coming soon)")

# Settings Page
elif page == "Settings":
    st.title("Settings")
    st.write("### Configure your MyHedgeFund app settings")
    st.write("(Settings options coming soon)")
