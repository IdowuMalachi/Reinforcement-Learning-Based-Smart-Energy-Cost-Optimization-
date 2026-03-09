import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.subtle {
    color: #5f6368;
    font-size: 1rem;
}
.card {
    border: 1px solid #e6e9ef;
    border-radius: 18px;
    padding: 18px 20px;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 14px;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 650;
    margin-bottom: 0.6rem;
}
.note-box {
    border-left: 5px solid #4f8bf9;
    background: #f7faff;
    padding: 14px 16px;
    border-radius: 10px;
    margin-top: 8px;
    margin-bottom: 8px;
}
.small {
    font-size: 0.95rem;
    color: #4b5563;
}
.metric-label {
    color: #6b7280;
    font-size: 0.9rem;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #16a34a;
}
</style>
""", unsafe_allow_html=True)

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

def estimate_grid_use(demand_kw: float, action: str, battery_kwh: float) -> float:
    if action == "Discharge battery":
        supplied = min(2.5, battery_kwh, demand_kw)
        return max(0.0, demand_kw - supplied)
    elif action == "Charge battery":
        return demand_kw + 1.0
    return demand_kw

def battery_status(level: float, capacity: float) -> str:
    pct = 100 * level / capacity if capacity else 0
    if pct >= 70:
        return "High"
    if pct >= 35:
        return "Moderate"
    return "Low"

st.sidebar.title("⚙️ Simulation Controls")
st.sidebar.caption("Adjust the system state to see how the decision engine responds.")

hour = st.sidebar.slider("Hour of day", 0, 23, 18)
demand_kw = st.sidebar.slider("Demand (kW)", 0.0, 8.0, 3.0, 0.1)
battery_kwh = st.sidebar.slider("Battery level (kWh)", 0.0, 10.0, 5.0, 0.1)
capacity_kwh = st.sidebar.slider("Battery capacity (kWh)", 2.0, 20.0, 10.0, 0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("### Purpose")
st.sidebar.write(
    "This app demonstrates the logic behind a reinforcement learning energy management project. "
    "It shows how a smart controller can reduce electricity cost using battery storage and time-of-use pricing."
)
st.sidebar.markdown("### Notes")
st.sidebar.write(
    "This is a presentation-ready simulation app. It explains the decision logic clearly, "
    "but it does not run the full training loop inside Streamlit."
)

price = time_of_use_price(hour)
action = recommend_action(hour, battery_kwh, demand_kw, capacity_kwh)
grid_use = estimate_grid_use(demand_kw, action, battery_kwh)
estimated_cost = grid_use * price

st.markdown('<div class="main-title">⚡ Smart Energy Optimizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtle">A reinforcement learning-inspired decision support app for energy cost optimization using demand, battery storage, and time-of-use pricing.</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card"><div class="metric-label">Hour</div><div class="metric-value">{hour:02d}:00</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><div class="metric-label">Electricity Price</div><div class="metric-value">${price:.2f}/kWh</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card"><div class="metric-label">Battery Status</div><div class="metric-value">{battery_status(battery_kwh, capacity_kwh)}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="card"><div class="metric-label">Estimated Grid Cost</div><div class="metric-value">${estimated_cost:.2f}</div></div>', unsafe_allow_html=True)

left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Project Purpose</div>', unsafe_allow_html=True)
    st.write(
        "The purpose of this project is to show how intelligent energy control can reduce electricity cost. "
        "The system uses household demand as the load signal, a simulated battery as storage, and a time-of-use tariff as the pricing mechanism. "
        "The decision engine recommends whether the system should charge the battery, discharge it, or stay idle."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current System State</div>', unsafe_allow_html=True)
    state_df = pd.DataFrame({
        "Variable": ["Hour", "Demand", "Battery Level", "Battery Capacity", "Grid Price"],
        "Value": [f"{hour}:00", f"{demand_kw:.1f} kW", f"{battery_kwh:.1f} kWh", f"{capacity_kwh:.1f} kWh", f"${price:.2f}/kWh"]
    })
    st.dataframe(state_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tariff Schedule</div>', unsafe_allow_html=True)
    tariff_df = pd.DataFrame({
        "Hour": list(range(24)),
        "Price ($/kWh)": [time_of_use_price(h) for h in range(24)]
    }).set_index("Hour")
    st.line_chart(tariff_df)
    st.markdown('<div class="small">The tariff is lowest overnight, moderate during daytime, and highest during evening peak hours.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommended Action</div>', unsafe_allow_html=True)

    if action == "Discharge battery":
        st.error(f"Action: {action}")
    elif action == "Charge battery":
        st.success(f"Action: {action}")
    else:
        st.info(f"Action: {action}")

    if action == "Discharge battery":
        explanation = (
            "The system is in a high-price period and there is usable energy in the battery. "
            "Discharging the battery helps reduce dependence on expensive grid electricity."
        )
    elif action == "Charge battery":
        explanation = (
            "The current period has low electricity cost and the battery has available capacity. "
            "Charging now allows the system to save cheaper energy for later use."
        )
    else:
        explanation = (
            "The current state does not strongly support charging or discharging. "
            "Remaining idle is the most balanced decision under these conditions."
        )

    st.markdown(f'<div class="note-box">{explanation}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Decision Notes</div>', unsafe_allow_html=True)
    st.write(
        "This app is designed for explanation and presentation. In the full project, a Q-learning agent is trained on many episodes to improve its policy over time. "
        "Here, the interface focuses on the logic, purpose, and practical meaning of each recommendation."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Project Components</div>', unsafe_allow_html=True)
    summary_df = pd.DataFrame({
        "Component": [
            "State variables",
            "Actions",
            "Reward objective",
            "Pricing model",
            "Deployment style"
        ],
        "Description": [
            "Hour, demand, battery level",
            "Idle, charge battery, discharge battery",
            "Minimize total electricity cost",
            "Simulated time-of-use tariff",
            "Interactive Streamlit dashboard"
        ]
    })
    st.dataframe(summary_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">How to Read This App</div>', unsafe_allow_html=True)
st.write(
    "Start by adjusting the controls in the sidebar. The app updates the hour, demand, battery level, and electricity price. "
    "It then recommends an action and explains why that action is reasonable in the current state. "
    "This makes the project easier to present because the audience can immediately see the purpose, the logic, and the expected cost implication."
)
st.markdown('</div>', unsafe_allow_html=True)

st.caption(
    "Smart Energy Optimizer | Reinforcement learning-inspired presentation app for electricity cost optimization."
)
