import streamlit as st
import re
import pandas as pd

# Set page config
st.set_page_config(page_title="MyHedgeFund", layout="wide")

# Sidebar Navigation with larger text
st.sidebar.title("## Navigation")
st.sidebar.markdown("---")

pages = {
    "🏠 **Home**": "Home",
    "📈 **Trades**": "Trades",
    "🏆 **Leaderboard**": "Leaderboard",
    "⚙️ **Options Simulator**": "Options Simulator",
    "📊 **Position Simulator**": "Position Simulator",
    "🔧 **Settings**": "Settings"
}

page = st.sidebar.radio("### Select a Page", list(pages.keys()))
page = pages[page]

# Home Page: Portfolio Overview
if page == "Home":
    st.title("MyHedgeFund - Portfolio")
    
    # Portfolio Performance Metrics
    st.subheader("Portfolio Performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total P/L", "$5,000", "+10%")
    col2.metric("Total Gain", "$7,500", "12%")
    col3.metric("Portfolio Value", "$55,000")
    col4.metric("Total Positions", "3")
    
    st.write("### Active Positions")
    
    # Example position data
    positions = [
        {"Ticker": "AAPL", "P/L": "$1,500", "Gain": "5%", "Size": "$10,000"},
        {"Ticker": "TSLA", "P/L": "$2,000", "Gain": "8%", "Size": "$15,000"},
        {"Ticker": "AMZN", "P/L": "$1,500", "Gain": "7%", "Size": "$12,000"}
    ]
    
    for pos in positions:
        st.subheader(f"{pos['Ticker']} - {pos['P/L']} ({pos['Gain']})")
        st.write(f"**Position Size:** {pos['Size']}")
        
        # Example trades for each position
        trade_data = pd.DataFrame({
            "Trade Type": ["Buy", "Buy", "Sell"],
            "Quantity": [50, 30, 20],
            "Price": [150.0, 160.0, 170.0],
            "Date": ["2024-01-10", "2024-02-05", "2024-02-20"]
        })
        st.table(trade_data)

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
