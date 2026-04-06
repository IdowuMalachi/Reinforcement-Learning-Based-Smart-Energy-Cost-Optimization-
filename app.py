import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math

st.set_page_config(layout="wide")

st.title("⚡ Smart Energy Management (RL Demo)")
st.write("Compare Q-Learning, SARSA, DQN, and Rule-Based strategies")

# =============================
# CONFIG
# =============================
capacity = 10.0

def price(hour):
    if 0 <= hour < 6:
        return 0.10
    elif 6 <= hour < 17:
        return 0.18
    elif 17 <= hour < 22:
        return 0.30
    return 0.15

# =============================
# POLICIES (SIMULATED LOGIC)
# =============================
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
    return random.choice([0,1,2])

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

# =============================
# SIMULATION STEP
# =============================
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
    cost = grid * p
    return battery, cost

# =============================
# USER INPUT
# =============================
col1, col2, col3 = st.columns(3)

with col1:
    start_hour = st.slider("Start Hour", 0, 23, 12)
    demand = st.slider("Base Demand (kW)", 0.5, 6.0, 2.5)

with col2:
    steps = st.slider("Simulation Steps", 10, 100, 24)
    battery_init = st.slider("Initial Battery", 0.0, 10.0, 5.0)

with col3:
    algo = st.selectbox("Algorithm", ["Rule-Based", "Q-Learning", "SARSA", "DQN"])
    compare = st.checkbox("Compare All", True)

algorithms = ["Rule-Based", "Q-Learning", "SARSA", "DQN"] if compare else [algo]

# =============================
# RUN SIMULATION
# =============================
results = {}

for a in algorithms:
    battery = battery_init
    cost_list = []
    battery_list = []

    for t in range(steps):
        hour = (start_hour + t) % 24
        d = demand + np.sin(t/3) + random.uniform(-0.2,0.2)

        action = get_action(a, hour, battery, d)
        battery, cost = step(battery, action, d, hour)

        cost_list.append(cost)
        battery_list.append(battery)

    results[a] = {
        "cost": cost_list,
        "battery": battery_list,
        "total_cost": sum(cost_list)
    }

# =============================
# OUTPUT
# =============================
st.subheader("📊 Total Cost Comparison")

for k,v in results.items():
    st.write(f"{k}: **{v['total_cost']:.2f}**")

# =============================
# PLOTS
# =============================
st.subheader("📉 Cost Over Time")

for k,v in results.items():
    plt.plot(v["cost"], label=k)

plt.legend()
plt.title("Cost per Step")
st.pyplot(plt)
plt.clf()

st.subheader("🔋 Battery Level")

for k,v in results.items():
    plt.plot(v["battery"], label=k)

plt.legend()
plt.title("Battery Usage")
st.pyplot(plt)
plt.clf()
