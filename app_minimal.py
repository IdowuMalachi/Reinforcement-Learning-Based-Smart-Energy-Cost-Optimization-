import streamlit as st

st.set_page_config(page_title="RL Energy Dashboard", page_icon="⚡", layout="centered")

def tariff(hour):
    if 0 <= hour < 6:
        return 0.10
    if 6 <= hour < 17:
        return 0.18
    if 17 <= hour < 22:
        return 0.30
    return 0.15

st.title("RL Energy Management Dashboard")
st.write("A simplified deployment demo for reinforcement learning-based energy cost optimization.")

hour = st.slider("Hour of day", 0, 23, 18)
demand = st.slider("Demand (kW)", 0.0, 8.0, 3.0, 0.1)
battery = st.slider("Battery level (kWh)", 0.0, 10.0, 5.0, 0.1)

price = tariff(hour)

if price >= 0.30 and battery > 1.0 and demand > 0.5:
    action = "Discharge battery"
elif price <= 0.10 and battery < 9.0:
    action = "Charge battery"
else:
    action = "Stay idle"

st.subheader("Current State")
st.write("Hour:", hour)
st.write("Demand (kW):", demand)
st.write("Battery level (kWh):", battery)
st.write("Electricity price ($/kWh):", price)

st.subheader("Recommended Action")
st.write(action)

if action == "Discharge battery":
    grid_use = max(0.0, demand - min(2.5, battery, demand))
elif action == "Charge battery":
    grid_use = demand + 1.0
else:
    grid_use = demand

cost = grid_use * price
st.subheader("Estimated One-Hour Grid Cost")
st.write(round(cost, 2))

st.subheader("Tariff Table")
st.table({
    "Hour Range": ["00-05", "06-16", "17-21", "22-23"],
    "Price ($/kWh)": [0.10, 0.18, 0.30, 0.15]
})

st.caption("This app is a lightweight presentation demo and does not run the full Q-learning training loop.")
