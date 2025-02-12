import streamlit as st
import re
import pandas as pd
import plotly.graph_objects as go
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.toolbox import Toolbox as t
from portfolio.portfolio import Portfolio
from portfolio.position import Position
from portfolio.trade import Trade
import time

# Set page config
st.set_page_config(page_title="MyHedgeFund", layout="wide")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# Login section
if not st.session_state.logged_in:
    st.title("Login")
    user = st.text_input("Credential")
    if st.button("Login"):
        # Replace with your own authentication logic
        if os.path.exists("data/" + user + ".json"):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
else:

    p = Portfolio(0)
    p = t.load_obj_from_json(p, ("data/" + st.session_state.user + ".json"))

    arePositions = False


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
            st.write("Data last updated: " + str(time.ctime())[10:-5])
            if not arePositions:
                st.title("Welcome to MyHedgeFund")
                st.write("### Let's get started by adding your positions in the trades section.")
            else:
                # Portfolio Performance Metrics
                st.subheader("Portfolio Performance")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total P/L", "$5,000", "+10%")
                col2.metric("Total Gain", "$7,500", "12%")
                col3.metric("Portfolio Value", "$55,000")
                col4.metric("Total Positions", "3")

                # Line chart with legend
                st.subheader("Market Overview")

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
                    y=[105, 107, 103, 110, 115],
                    mode="lines",
                    name="Fund Performance",
                    line=dict(color="green")
                ))

                fig.add_trace(go.Scatter(
                    x=["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
                    y=[103, 105, 104, 108, 110],
                    mode="lines",
                    name="SPY Index",
                    line=dict(color="blue")
                ))

                fig.update_layout(
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

                # Detailed Metrics Tile
                st.subheader("Detailed Portfolio Metrics")
                st.write("(More in-depth analytics coming soon)")


    # Positions Page
    elif page == "Positions":
        st.title("Positions")
        st.write("Active Positions")

        st.write("Data last updated: " + str(time.ctime())[10:-5])

        if not arePositions:
            st.write("No positions to display.")
            st.write("Go to trades to add your first position.")
        else:
            # position data
            positions = p.getPositions()
            
            #temporary price placeholder
            price = 10

            for pos in positions:
                with st.expander(f"{pos['Ticker']} - ({pos.getPercentPortfolio()}%)"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Mkt Value", pos.getMktValue(price))
                    col2.metric("Breakeven", pos.getBreakeven())
                    col3.metric("% Gain", pos.getPercentPL(price))
                    col4.metric("$ Gain", pos.getDollarPL(price))

                    # Example trades for each position
                    trade_data = pd.DataFrame({
                        "Type": ["Buy", "Buy", "Sell"],
                        "Quantity": [50, 30, 20],
                        "Price": [150.0, 160.0, 170.0],
                        "$ PL": ["2024-01-10", "2024-02-05", "2024-02-20"],
                        "% PL": ["2024-01-10", "2024-02-05", "2024-02-20"],
                        "Mkt Value": ["2024-01-10", "2024-02-05", "2024-02-20"],
                        "% Position": ["2024-01-10", "2024-02-05", "2024-02-20"]
                    })

                    # Convert DataFrame to HTML with larger font and wider columns
                    trade_data_html = trade_data.to_html(index=False)
                    trade_data_html = trade_data_html.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="font-size:20px; width:100%;">')
                    trade_data_html = trade_data_html.replace('<th>', '<th style="padding: 10px;">')
                    trade_data_html = trade_data_html.replace('<td>', '<td style="padding: 10px;">')

                    st.write(trade_data_html, unsafe_allow_html=True)

                    # Option to add options table
                    if st.checkbox(f"Show Options for {pos['Ticker']}"):
                        options_data = pd.DataFrame({
                            "Type": ["Call", "Put"],
                            "Strike": [155.0, 145.0],
                            "Expiry": ["2024-06-21", "2024-06-21"],
                            "Premium": [5.2, 4.3]
                        })
                        options_data_html = options_data.to_html(index=False)
                        options_data_html = options_data_html.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" style="font-size:20px; width:80%;">')
                        options_data_html = options_data_html.replace('<th>', '<th style="padding: 10px;">')
                        options_data_html = options_data_html.replace('<td>', '<td style="padding: 10px;">')
                        st.write(options_data_html, unsafe_allow_html=True)

    # Trades Page
    elif page == "Trades":
        st.title("Trades")
        st.write("### Add a new trade")

        temp = {
            "ticker": None, "price": None, "quantity": None, "trade_type": None, "asset": None, "strike": None, "expiry": None
        }

        temp["asset"] = st.selectbox("Select Asset Type", ["Stock", "Call", "Put"], key="trade_type")

        def validate_ticker_input(ticker):
            return re.sub(r'[^A-Z]', '', ticker.upper())

        temp["ticker"] = st.text_input("Ticker Symbol", key="ticker")
        temp["ticker"] = validate_ticker_input(temp["ticker"])

        temp["price"] = st.number_input("Price", step=0.01, key="price")
        temp["quantity"] = st.number_input("Quantity", step=1, key="quantity")
        temp["trade_type"] = st.selectbox("Trade Type", ["Long", "Sell", "Short", "Cover"], key="trade_action")

        if temp["asset"] == "Call" or temp["asset"] == "Put":
            temp["strike"] = st.number_input("Strike Price", step=0.01, key="strike")
            temp["expiry"] = st.date_input("Expiry Date", key="expiry")

        if st.button("Submit Trade"):
            arePositions = True
            p.addTrade(Trade(temp["ticker"], temp["price"], temp["quantity"], temp["trade_type"], temp["asset"], temp["strike"], temp["expiry"]))
            t.save_to_json(p, "data/" + st.session_state.user + ".json")

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

        st.subheader("Cash on Hand")

        # Input box to change cash on hand value
        new_cash = st.number_input("Edit cash on hand value:", value=p.cash, step=0.01)

        # Button to save the new value
        if st.button("Save"):
            p.cash = new_cash
            t.save_to_json(p, "data/portfolio.json")
            st.success("Cash on hand value saved successfully!")