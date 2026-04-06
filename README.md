⚡ Reinforcement Learning for Smart Energy Management

A comprehensive reinforcement learning project that applies Q-Learning, SARSA, DQN, and Double DQN to optimize electricity cost and battery storage usage in a simulated smart energy system.

📌 Project Overview

This project explores how reinforcement learning (RL) can be used to make intelligent decisions in energy systems, particularly for:

Reducing electricity costs
Optimizing battery storage usage
Adapting to dynamic demand and pricing conditions

Unlike traditional rule-based systems, this project demonstrates how RL agents can learn optimal strategies through interaction with the environment.

🎯 Objectives
Develop an RL-based energy management system
Compare multiple algorithms:
Q-Learning
SARSA
Deep Q-Network (DQN)
Double DQN
Evaluate performance using:
Cost reduction
Reward convergence
Battery utilization
Deploy an interactive dashboard using Streamlit
🧠 Algorithms Implemented
1. Q-Learning
Off-policy algorithm
Uses Q-table
Fast learning but unstable in some cases
2. SARSA
On-policy algorithm
More stable than Q-Learning
Learns based on actual actions taken
3. DQN (Deep Q-Network)
Uses neural networks
Handles continuous state spaces
Better generalization
4. Double DQN
Improves DQN
Reduces overestimation bias
More stable learning
⚙️ System Architecture

The system consists of:

🔹 Environment
Electricity demand (real dataset)
Battery storage system
Time-of-use pricing
🔹 Agent
Observes system state
Selects action:
Charge
Discharge
Idle
🔹 Reward Function
Reward = – (Electricity Cost + Battery Degradation Penalty)
📊 Dataset
Individual Household Electric Power Consumption Dataset
Used as real demand signal
Includes:
Global active power
Time-based consumption patterns
🔄 Workflow
Data preprocessing
Feature engineering
Environment simulation
Model training (RL algorithms)
Evaluation
Deployment (Streamlit dashboard)
📈 Key Results
🔹 Reward Convergence
All algorithms show learning over time
Double DQN shows best stability
🔹 Cost Optimization
RL outperforms rule-based strategy
DQN and Double DQN achieve lowest costs
🔹 Battery Utilization
RL learns:
Charge during low price
Discharge during peak
📊 Visualizations

The project includes:

Training reward curves
Loss curves (DQN & Double DQN)
Cost comparison charts
Battery usage plots
Action distribution analysis
🖥️ Streamlit Dashboard

An interactive dashboard was developed to:

Simulate energy scenarios
Compare algorithms in real-time
Visualize:
Cost trends
Battery levels
Demand patterns
Provide recommendations

## Streamlit
Run:
    streamlit run app.py
    https://53566xkvoxvnxrdc4tzcjy.streamlit.app/ 
