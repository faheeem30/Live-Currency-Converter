import streamlit as st
import requests
import sqlite3
from datetime import datetime
import plotly.graph_objects as go

# ---- PAGE SETTINGS ----
st.set_page_config(page_title="💱 Currency Converter", page_icon="💰", layout="centered")
st.title("💱 Live Currency Converter (with History & Trend)")
st.write("Real-time currency converter using Frankfurter API + SQLite storage")

# ---- DATABASE SETUP ----
conn = sqlite3.connect("conversions.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base TEXT,
        target TEXT,
        amount REAL,
        converted REAL,
        rate REAL,
        date TEXT
    )
""")
conn.commit()

# ---- FETCH CURRENCIES DYNAMICALLY ----
try:
    response = requests.get("https://api.frankfurter.app/currencies")
    currencies_data = response.json()  # dict like {"USD":"United States Dollar", ...}
    # Dropdown: "USD - United States Dollar"
    currency_options = [f"{code} - {name}" for code, name in currencies_data.items()]
except Exception as e:
    st.error(f"⚠️ Could not fetch currency list: {e}")
    currency_options = [
        "USD - United States Dollar", "EUR - Euro", "INR - Indian Rupee",
        "GBP - British Pound", "AUD - Australian Dollar", "CAD - Canadian Dollar",
        "JPY - Japanese Yen", "CNY - Chinese Yuan", "SGD - Singapore Dollar",
        "CHF - Swiss Franc"
    ]  # fallback

# ---- UI INPUTS ----
col1, col2 = st.columns(2)
with col1:
    base_choice = st.selectbox(
        "From Currency", currency_options,
        index=[i for i, c in enumerate(currency_options) if c.startswith("USD")][0]
    )
    base = base_choice.split(" - ")[0]  # extract code
with col2:
    target_choice = st.selectbox(
        "To Currency", currency_options,
        index=[i for i, c in enumerate(currency_options) if c.startswith("INR")][0]
    )
    target = target_choice.split(" - ")[0]  # extract code

amount = st.number_input("Enter Amount", min_value=0.0, value=1.0, step=0.5)

# ---- CONVERT BUTTON ----
if st.button("Convert 💰"):
    try:
        url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
        response = requests.get(url)
        data = response.json()

        if "rates" in data:
            rate = data["rates"][target]
            converted = amount * rate
            st.success(f"✅ {amount} {base} = {converted:.2f} {target}")
            st.caption(f"1 {base} = {rate:.4f} {target} | Updated: {data['date']}")

            # --- Save to Database ---
            cur.execute(
                "INSERT INTO history (base, target, amount, converted, rate, date) VALUES (?, ?, ?, ?, ?, ?)",
                (base, target, amount, converted, rate, data["date"])
            )
            conn.commit()

            # Keep only last 10 entries
            cur.execute("DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT 10)")
            conn.commit()
        else:
            st.error("❌ Unable to fetch data.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# ---- HISTORY DROPDOWN ----
st.subheader("📜 Last 10 Conversions")
cur.execute("SELECT base, target, amount, converted, rate, date FROM history ORDER BY id DESC")
rows = cur.fetchall()

if rows:
    options = [
        f"{r[0]} → {r[1]} | {r[2]} {r[0]} = {r[3]:.2f} {r[1]} (Rate: {r[4]:.4f}, Date: {r[5]})"
        for r in rows
    ]
    choice = st.selectbox("Select a past conversion:", options)
else:
    st.info("No conversion history yet.")

# ---- HISTORICAL TREND ----
st.subheader("📊 Historical Trend (Interactive Plotly)")

with st.form("trend_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date", value=datetime(2024, 1, 1).date(),
            min_value=datetime(1999,1,1).date()
        )
    with col2:
        end_date = st.date_input("End Date", value=datetime.now().date())
    submitted = st.form_submit_button("Show Trend")

if submitted:
    if start_date >= end_date:
        st.warning("⚠️ Invalid date range (start < end).")
    else:
        try:
            url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base}&to={target}"
            response = requests.get(url)
            data = response.json()

            if "rates" in data and len(data["rates"]) > 0:
                dates = list(data["rates"].keys())
                rates = [r[target] for r in data["rates"].values()]

                # Plotly interactive chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, y=rates, mode='lines+markers',
                    line=dict(color='royalblue', width=2),
                    marker=dict(size=6),
                    name=f"{base}/{target}"
                ))
                fig.update_layout(
                    title=f"{base} → {target} Exchange Rate Trend ({start_date} to {end_date})",
                    xaxis_title="Date",
                    yaxis_title="Exchange Rate",
                    template="plotly_white",
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)

                st.success(f"✅ Showing rates from {start_date} to {end_date}")
            else:
                st.warning("No data available for this date range.")
        except Exception as e:
            st.error(f"⚠️ Error fetching historical data: {e}")
