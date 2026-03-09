import streamlit as st
import pandas as pd

st.set_page_config(page_title="RL Energy Management Dashboard", page_icon="⚡", layout="centered")
st.title("⚡ Reinforcement Learning Energy Management Project")
st.write(
    "This dashboard explains a reinforcement learning project built from the "
    "`household_power_consumption` dataset. The dataset provides real demand signals, "
    "while battery behavior and electricity prices are simulated to create an RL environment."
)

solar = st.slider("Simulated solar generation (kW)", 0.0, 8.0, 2.0, 0.1)
battery = st.slider("Battery level (kWh)", 0.0, 10.0, 5.0, 0.1)
demand = st.slider("Demand (kW)", 0.0, 8.0, 3.0, 0.1)
hour = st.slider("Hour of day", 0, 23, 18)

def price(hour):
    if 0 <= hour < 6:
        return 0.10
    elif 6 <= hour < 17:
        return 0.18
    elif 17 <= hour < 22:
        return 0.30
    return 0.15

current_price = price(hour)
st.write(f"**Simulated electricity price:** ${current_price:.2f}/kWh")

if hour < 6 and battery < 8:
    action = "Charge battery from grid"
elif 17 <= hour < 22 and battery > 1:
    action = "Discharge battery to reduce peak-time cost"
else:
    action = "Stay idle / use normal supply"

st.success(f"Recommended action: **{action}**")

summary_df = pd.DataFrame({
    "Component": ["State", "Actions", "Reward"],
    "Description": [
        "Hour, demand, battery level",
        "Idle, charge battery, discharge battery",
        "Negative cost, encouraging lower electricity cost"
    ]
})
st.dataframe(summary_df, use_container_width=True)
