import streamlit as st
import json
#from scripts import toolbox
#from portfolio import Portfolio



# Streamlit UI
st.title("📈 Portfolio Tracker")

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Trade", "View Positions"])

# 1. Dashboard
if menu == "Dashboard":
    st.header("📊 Portfolio Overview")

    if False:
        for position in portfolio["positions"]:
            st.subheader(f"📌 {position['symbol']}")
            st.write(f"**Type:** {position['position_type']}")
            st.write(f"**Quantity:** {position['quantity']}")
            st.write(f"**Average Price:** ${position['average_price']:.2f}")
    else:
        st.info("No positions found. Add a trade to get started.")

# 2. Add Trade
elif False: #menu == "Add Trade":
    st.header("➕ Add a Trade")

    with st.form("trade_form"):
        symbol = st.text_input("Symbol (e.g., AAPL, SPY)", max_chars=10)
        trade_type = st.selectbox("Trade Type", ["BUY", "SELL", "SHORT_SELL", "COVER_SHORT"])
        price = st.number_input("Price", min_value=0.01, format="%.2f")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        
        # Optional fields for options trading
        option_type = st.selectbox("Option Type (Optional)", ["None", "CALL", "PUT"])
        strike_price = st.number_input("Strike Price (if option)", min_value=0.0, format="%.2f")
        expiration_date = st.date_input("Expiration Date (if option)")

        submitted = st.form_submit_button("Add Trade")

        if submitted:
            new_trade = {
                "trade_id": f"T{len(portfolio['positions']) + 1}",
                "symbol": symbol,
                "trade_type": trade_type,
                "price": price,
                "quantity": quantity,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            if option_type != "None":
                new_trade.update({
                    "option_type": option_type,
                    "strike_price": strike_price,
                    "expiration_date": expiration_date.isoformat()
                })

            # Find existing position or create a new one
            for position in portfolio["positions"]:
                if position["symbol"] == symbol:
                    position["trades"].append(new_trade)
                    break
            else:
                portfolio["positions"].append({
                    "symbol": symbol,
                    "position_type": "OPTION" if option_type != "None" else "EQUITY",
                    "average_price": price,
                    "quantity": quantity,
                    "trades": [new_trade]
                })

            save_portfolio(portfolio)
            st.success(f"Trade added for {symbol}!")

# 3. View Positions
elif False: #menu == "View Positions":
    st.header("📄 Positions")

    if portfolio["positions"]:
        for position in portfolio["positions"]:
            with st.expander(f"📌 {position['symbol']} - {position['position_type']}"):
                st.write(f"**Quantity:** {position['quantity']}")
                st.write(f"**Average Price:** ${position['average_price']:.2f}")

                st.subheader("Trade History")
                for trade in position["trades"]:
                    st.write(f"📝 {trade['trade_id']} - {trade['trade_type']} {trade['quantity']} @ ${trade['price']}")
    else:
        st.info("No positions available.")

st.sidebar.text("💾 Data is automatically saved.")
