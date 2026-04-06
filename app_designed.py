import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import math

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="Smart Energy Management Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #0f172a;
}
.kpi-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
    border-left: 6px solid #2563eb;
}
.info-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 14px;
}
.hero {
    background: linear-gradient(135deg, #0f172a, #1d4ed8);
    color: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    margin-bottom: 18px;
}
.small-note {
    font-size: 0.92rem;
    color: #475569;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>⚡ Smart Energy Management Dashboard</h1>
    <p style="font-size:17px;">
        A reinforcement learning demo for comparing <b>Q-Learning</b>, <b>SARSA</b>, <b>DQN</b>, and
        a <b>Rule-Based strategy</b> for battery charging and electricity cost optimization.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("⚙️ Simulation Control Panel")
st.sidebar.markdown("Adjust the scenario settings below and explore how each algorithm manages battery charging and electricity cost.")

start_hour = st.sidebar.slider("Start Hour", 0, 23, 12)
demand = st.sidebar.slider("Base Demand (kW)", 0.5, 6.0, 2.5)
steps = st.sidebar.slider("Simulation Steps", 10, 100, 24)
battery_init = st.sidebar.slider("Initial Battery (kWh)", 0.0, 10.0, 5.0)
algo = st.sidebar.selectbox("Select Primary Algorithm", ["Rule-Based", "Q-Learning", "SARSA", "DQN"])
compare = st.sidebar.checkbox("Compare All Algorithms", True)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ How to Use")
st.sidebar.markdown("""
1. Set the **start hour** and **base demand**.  
2. Select how many **simulation steps** you want.  
3. Choose the **initial battery level**.  
4. Pick one algorithm or compare all.  
5. Review the cost, battery trends, recommendations, and analysis.
""")

# ============================================================
# CONFIG
# ============================================================
capacity = 10.0

def price(hour):
    if 0 <= hour < 6:
        return 0.10
    elif 6 <= hour < 17:
        return 0.18
    elif 17 <= hour < 22:
        return 0.30
    return 0.15

# ============================================================
# POLICIES
# ============================================================
def rule_based(hour, battery):
    if hour < 6 and battery < 8:
        return 1
    elif 17 <= hour < 22 and battery > 2:
        return 2
    return 0

def q_learning(hour, battery, demand):
    if price(hour) > 0.25 and battery > 2:
        return 2
    elif price(hour) < 0.15 and battery < 8:
        return 1
    return random.choice([0, 1, 2])

def sarsa(hour, battery, demand):
    if price(hour) > 0.25 and battery > 3:
        return 2
    elif price(hour) < 0.15 and battery < 7:
        return 1
    return 0

def dqn(hour, battery, demand):
    if demand > 3 and battery > 2:
        return 2
    elif price(hour) < 0.15:
        return 1
    return 0

def get_action(algo, hour, battery, demand):
    if algo == "Rule-Based":
        return rule_based(hour, battery)
    if algo == "Q-Learning":
        return q_learning(hour, battery, demand)
    if algo == "SARSA":
        return sarsa(hour, battery, demand)
    return dqn(hour, battery, demand)

def action_name(action):
    return {0: "Idle", 1: "Charge", 2: "Discharge"}[action]

# ============================================================
# SIMULATION STEP
# ============================================================
def step(battery, action, demand, hour):
    p = price(hour)

    if action == 1:  # charge
        battery += 1.5
        grid = demand + 1.5
    elif action == 2:  # discharge
        used = min(1.5, battery)
        battery -= used
        grid = demand - used
    else:
        grid = demand

    battery = max(0, min(capacity, battery))
    cost = max(grid, 0) * p
    return battery, cost, p

# ============================================================
# RUN SIMULATION
# ============================================================
algorithms = ["Rule-Based", "Q-Learning", "SARSA", "DQN"] if compare else [algo]
results = {}
detail_rows = []

for a in algorithms:
    battery = battery_init
    cost_list = []
    battery_list = []
    demand_list = []
    price_list = []
    action_list = []

    for t in range(steps):
        hour = (start_hour + t) % 24
        d = demand + np.sin(t / 3) + random.uniform(-0.2, 0.2)
        d = max(0.3, d)

        action = get_action(a, hour, battery, d)
        battery, cost, p = step(battery, action, d, hour)

        cost_list.append(cost)
        battery_list.append(battery)
        demand_list.append(d)
        price_list.append(p)
        action_list.append(action_name(action))

        detail_rows.append({
            "Algorithm": a,
            "Step": t + 1,
            "Hour": hour,
            "Demand_kW": round(d, 3),
            "Price": round(p, 2),
            "Battery_kWh": round(battery, 3),
            "Action": action_name(action),
            "Cost": round(cost, 3)
        })

    results[a] = {
        "cost": cost_list,
        "battery": battery_list,
        "demand": demand_list,
        "price": price_list,
        "actions": action_list,
        "total_cost": sum(cost_list),
        "avg_cost": np.mean(cost_list),
        "final_battery": battery_list[-1],
        "max_battery": max(battery_list),
        "min_battery": min(battery_list)
    }

details_df = pd.DataFrame(detail_rows)
summary_df = pd.DataFrame([
    {
        "Algorithm": k,
        "Total Cost": round(v["total_cost"], 3),
        "Average Cost": round(v["avg_cost"], 3),
        "Final Battery": round(v["final_battery"], 3),
        "Max Battery": round(v["max_battery"], 3),
        "Min Battery": round(v["min_battery"], 3)
    }
    for k, v in results.items()
]).sort_values("Total Cost")

best_algo = summary_df.iloc[0]["Algorithm"]
best_cost = summary_df.iloc[0]["Total Cost"]

# ============================================================
# KPI SECTION
# ============================================================
st.subheader("📌 Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Best Algorithm</h3>
        <h2>{best_algo}</h2>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Lowest Total Cost</h3>
        <h2>{best_cost:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Simulation Steps</h3>
        <h2>{steps}</h2>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Initial Battery</h3>
        <h2>{battery_init:.1f} kWh</h2>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SUMMARY + RECOMMENDATION
# ============================================================
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("📊 Algorithm Performance Summary")
    st.dataframe(summary_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("🧠 Recommendation")
    st.write(f"Based on the current simulation, **{best_algo}** achieved the lowest total cost.")
    st.write(
        "This suggests that under the selected demand, battery, and pricing conditions, "
        f"**{best_algo}** provided the most effective battery scheduling strategy."
    )
    st.markdown("**Operational note:**")
    st.write(
        "When demand is high and prices peak, stronger discharge decisions can reduce grid dependency. "
        "When prices are low, charging becomes more beneficial."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CHARTS
# ============================================================
st.subheader("📉 Cost Trend Analysis")
fig1, ax1 = plt.subplots(figsize=(10, 4))
for k, v in results.items():
    ax1.plot(v["cost"], label=k, linewidth=2)
ax1.set_title("Cost per Simulation Step")
ax1.set_xlabel("Step")
ax1.set_ylabel("Cost")
ax1.legend()
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

st.subheader("🔋 Battery Level Analysis")
fig2, ax2 = plt.subplots(figsize=(10, 4))
for k, v in results.items():
    ax2.plot(v["battery"], label=k, linewidth=2)
ax2.set_title("Battery Level Over Time")
ax2.set_xlabel("Step")
ax2.set_ylabel("Battery (kWh)")
ax2.legend()
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Demand Profile")
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    sample_algo = algorithms[0]
    ax3.plot(results[sample_algo]["demand"], linewidth=2)
    ax3.set_title(f"Demand Pattern ({sample_algo} Scenario)")
    ax3.set_xlabel("Step")
    ax3.set_ylabel("Demand (kW)")
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)

with c2:
    st.subheader("💲 Price Profile")
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ax4.plot(results[sample_algo]["price"], linewidth=2)
    ax4.set_title("Electricity Price Over Time")
    ax4.set_xlabel("Step")
    ax4.set_ylabel("Price")
    ax4.grid(True, alpha=0.3)
    st.pyplot(fig4)

# ============================================================
# ACTION ANALYSIS
# ============================================================
st.subheader("🎯 Action Analysis")
action_summary = (
    details_df.groupby(["Algorithm", "Action"])
    .size()
    .reset_index(name="Count")
)
st.dataframe(action_summary, use_container_width=True)

# ============================================================
# DETAILED ANALYSIS TEXT
# ============================================================
st.subheader("📝 Detailed Analysis")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.write(
    "This dashboard compares reinforcement learning and rule-based strategies for energy cost optimization. "
    "Q-Learning uses exploratory decisions and may produce more variable behavior. "
    "SARSA tends to behave more conservatively because it updates based on the current policy. "
    "DQN represents a more advanced strategy, designed here to react strongly to high-demand states. "
    "The rule-based method follows simple handcrafted logic based on time-of-use pricing."
)
st.write(
    "The cost plot shows how each algorithm performs across the simulation horizon, while the battery chart "
    "illustrates storage utilization. A lower total cost indicates a more effective balance between charging at low-price periods "
    "and discharging during expensive periods."
)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# NOTES AND LIMITATIONS
# ============================================================
n1, n2 = st.columns(2)

with n1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("📌 Notes")
    st.write("- This dashboard is a demonstration environment based on simplified decision logic.")
    st.write("- Charging and discharging are constrained by a fixed battery capacity.")
    st.write("- Demand is simulated with a sinusoidal trend and small random variation.")
    st.write("- The comparison is useful for illustrating policy behavior and dashboard deployment.")
    st.markdown('</div>', unsafe_allow_html=True)

with n2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("⚠️ Limitations")
    st.write("- The current implementation does not load trained external model files.")
    st.write("- Battery degradation is not fully modeled in a physical sense.")
    st.write("- Pricing is based on fixed time-of-use assumptions.")
    st.write("- A real deployment can be extended with actual dataset input and trained RL policies.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# HOW TO INTERPRET
# ============================================================
st.subheader("📚 How to Interpret the Dashboard")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.write(
    "Use the KPI cards to identify the best-performing algorithm quickly. "
    "The summary table ranks each algorithm by total cost. "
    "The cost chart helps assess operational efficiency over time, "
    "while the battery chart shows whether the strategy is aggressively charging, conservatively storing, "
    "or frequently discharging energy. The action analysis section reveals behavioral patterns such as how often "
    "an algorithm chooses to charge, discharge, or remain idle."
)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RAW DATA
# ============================================================
with st.expander("🔍 View Detailed Simulation Data"):
    st.dataframe(details_df, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Smart Energy Management Dashboard | Reinforcement Learning Demo using Q-Learning, SARSA, DQN, and Rule-Based control")
