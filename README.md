# Reinforcement Learning Energy Management Project

This package contains a complete reinforcement learning project built from the
`household_power_consumption.txt` dataset inside `archive.zip`.

## Included files
- `rl_energy_management.py` — main Python script
- `RL_Energy_Management_Notebook.ipynb` — Jupyter notebook version
- `app.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies
- `project_report_outline.md` — report-ready writeup outline

## Project idea
The uploaded dataset provides real electricity demand data. Since it does not include
solar generation, battery state, or electricity pricing, this project builds a
simulated smart energy management environment where:
- demand comes from the real dataset
- battery storage is simulated
- electricity tariff is simulated by time-of-use pricing
- an RL agent learns when to charge, discharge, or stay idle

## Actions
- 0 = idle
- 1 = charge battery from grid
- 2 = discharge battery to meet demand

## How to run
1. Place `archive.zip` in the same folder as the script/notebook, or update the path.
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python rl_energy_management.py

## Streamlit
Run:
    streamlit run app.py
    https://53566xkvoxvnxrdc4tzcjy.streamlit.app/ 
