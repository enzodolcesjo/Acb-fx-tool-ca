import pandas as pd

def process(trades_df, opening_df, fx_df):
    summary = {}
    audit = []

    opening_dict = {
        row["Symbol"]: {
            "quantity": row["Quantity"],
            "acb_cad": row["CostBasisMoney"] * fx_df[fx_df["FXCurrency"] == row["CurrencyPrimary"]]["CostPrice"].values[0]
            if row["CurrencyPrimary"] != "CAD" else row["CostBasisMoney"],
            "fx_loan_usd": row["CostBasisMoney"] if row["CurrencyPrimary"] != "CAD" else 0.0,
            "currency": row["CurrencyPrimary"],
            "fx_rate_open": fx_df[fx_df["FXCurrency"] == row["CurrencyPrimary"]]["CostPrice"].values[0]
            if row["CurrencyPrimary"] != "CAD" else 1.0
        }
        for _, row in opening_df.iterrows()
    }

    running = {}

    for _, row in trades_df.sort_values("Date").iterrows():
        symbol = row["Symbol"]
        currency = row[row.index[0]]
        tx_type = row["Buy/Sell"]
        qty = row["Quantity"]
        fx_rate = row["FXRateToBase"]
        proceeds_fx = row["Proceeds"]
        comm_fx = row["IBCommission"]
        date = row["Date"]

        if symbol not in running:
            open_info = opening_dict.get(symbol, {
                "quantity": 0, "acb_cad": 0, "fx_loan_usd": 0,
                "currency": currency, "fx_rate_open": 1.0
            })
            running[symbol] = {
                "shares": open_info["quantity"],
                "acb_cad": open_info["acb_cad"],
                "fx_loan_usd": open_info["fx_loan_usd"],
                "fx_weighted_cad": open_info["fx_loan_usd"] * open_info["fx_rate_open"]
            }

        state = running[symbol]

        if tx_type == "BUY":
            total_cad = proceeds_fx * fx_rate + comm_fx * fx_rate if currency != "CAD" else proceeds_fx + comm_fx
            state["acb_cad"] += total_cad
            state["shares"] += qty
            if currency != "CAD":
                state["fx_loan_usd"] += proceeds_fx
                state["fx_weighted_cad"] += proceeds_fx * fx_rate

        elif tx_type == "SELL" and state["shares"] >= qty:
            acb_per_share = state["acb_cad"] / state["shares"]
            acb_reduction = acb_per_share * qty

            proceeds_cad = proceeds_fx * fx_rate if currency != "CAD" else proceeds_fx
            comm_cad = comm_fx * fx_rate if currency != "CAD" else comm_fx
            net_proceeds = proceeds_cad - comm_cad
            cap_gain = net_proceeds - acb_reduction

            fx_gain = 0.0
            if currency != "CAD":
                fx_to_repay = state["fx_loan_usd"] * (qty / state["shares"])
                avg_fx_rate = state["fx_weighted_cad"] / state["fx_loan_usd"]
                fx_gain = fx_to_repay * (avg_fx_rate - fx_rate)
                state["fx_loan_usd"] -= fx_to_repay
                state["fx_weighted_cad"] -= fx_to_repay * avg_fx_rate

            audit.append({
                "Date": date,
                "Symbol": symbol,
                "Quantity Sold": qty,
                "ACB/Share (CAD)": round(acb_per_share, 5),
                "ACB Reduction (CAD)": round(acb_reduction, 2),
                "Net Proceeds (CAD)": round(net_proceeds, 2),
                "Capital Gain (CAD)": round(cap_gain, 2),
                "FX Gain (CAD)": round(fx_gain, 2)
            })

            state["shares"] -= qty
            state["acb_cad"] -= acb_reduction

    for symbol, data in running.items():
        if data["shares"] > 0:
            summary[symbol] = {
                "Stock Ticker": symbol,
                "Total Shares on Hand": data["shares"],
                "Total ACB (CAD)": round(data["acb_cad"], 2),
                "ACB/Share (CAD)": round(data["acb_cad"] / data["shares"], 5)
            }

    return {
        "summary": list(summary.values()),
        "audit": audit
    }