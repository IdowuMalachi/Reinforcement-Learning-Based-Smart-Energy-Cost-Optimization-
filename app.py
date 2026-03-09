import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RL Energy Management Dashboard",
    page_icon="⚡",
    layout="wide"
)

def time_of_use_price(hour: int) -> float:
    if 0 <= hour < 6:
        return 0.10
    elif 6 <= hour < 17:
        return 0.18
    elif 17 <= hour < 22:
        return 0.30
    return 0.15

def recommend_action(hour: int, battery_kwh: float, demand_kw: float, capacity_kwh: float) -> str:
    price = time_of_use_price(hour)

    if price >= 0.30 and battery_kwh > 1.0 and demand_kw > 0.5:
        return "Discharge battery"

    if price <= 0.10 and battery_kwh < capacity_kwh - 1.0:
        return "Charge battery"

    return "Stay idle"

def estimate_grid_cost(hour: int, demand_kw: float, action: str, battery_kwh: float) -> float:
    price = time_of_use_price(hour)

    if action == "Discharge battery":
        supplied = min(2.5, battery_kwh, demand_kw)
        grid_usage = max(0.0, demand_kw - supplied)
    elif action == "Charge battery":
        grid_usage = demand_kw + 1.0
    else:
        grid_usage = demand_kw

    return grid_usage * price

st.title("RL Energy Management Dashboard")

st.write(
    "This dashboard presents a simplified reinforcement learning energy management concept "
    "using household demand, a simulated battery system, and time-of-use pricing."
)

st.sidebar.header("Simulation Inputs")

hour = st.sidebar.slider("Hour of day", 0, 23, 18)
demand_kw = st.sidebar.slider("Demand (kW)", 0.0, 8.0, 3.0, 0.1)
battery_kwh = st.sidebar.slider("Battery level (kWh)", 0.0, 10.0, 5.0, 0.1)
capacity_kwh = st.sidebar.slider("Battery capacity (kWh)", 2.0, 20.0, 10.0, 0.5)

price = time_of_use_price(hour)
action = recommend_action(hour, battery_kwh, demand_kw, capacity_kwh)
estimated_cost = estimate_grid_cost(hour, demand_kw, action, battery_kwh)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Hour", f"{hour}:00")
col2.metric("Electricity Price", f"${price:.2f}/kWh")
col3.metric("Battery Level", f"{battery_kwh:.1f} kWh")
col4.metric("Demand", f"{demand_kw:.1f} kW")

st.subheader("Recommended Action")

if action == "Discharge battery":
    st.error(f"Action: {action}")
elif action == "Charge battery":
    st.success(f"Action: {action}")
else:
    st.info(f"Action: {action}")

st.write(f"Estimated one-hour grid cost: ${estimated_cost:.2f}")

st.subheader("Why this action was selected")

if action == "Discharge battery":
    st.write(
        "The current hour is in a high-price period and the battery has enough stored energy, "
        "so the recommended action is to discharge the battery."
    )
elif action == "Charge battery":
    st.write(
        "The current hour is in a low-price period and the battery still has available capacity, "
        "so the recommended action is to charge the battery."
    )
else:
    st.write(
        "The current state does not strongly favor charging or discharging, "
        "so the recommended action is to remain idle."
    )

st.subheader("Tariff Schedule")

tariff_df = pd.DataFrame({
    "Hour": list(range(24)),
    "Price ($/kWh)": [time_of_use_price(h) for h in range(24)]
}).set_index("Hour")

st.line_chart(tariff_df)

st.subheader("Project Components")

summary_df = pd.DataFrame({
    "Component": [
        "State variables",
        "Actions",
        "Reward objective",
        "Pricing model",
        "Battery system"
    ],
    "Description": [
        "Hour of day, demand level, battery level",
        "Idle, charge battery, discharge battery",
        "Minimize total electricity cost",
        "Simulated time-of-use tariff",
        "Simulated storage with simple constraints"
    ]
})

st.dataframe(summary_df, use_container_width=True)

st.caption(
    "This is a lightweight presentation dashboard. It explains the reinforcement learning "
    "energy management concept without running full training inside the app."
)
