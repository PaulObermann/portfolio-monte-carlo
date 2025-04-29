import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# --- Helper functions ---

def simulate_investment(mean, sd, startmoney, T, nsim):
    """Run investment simulation and return final amounts and last path."""
    finalmoney = []
    last_money_path = []
    for _ in range(int(nsim)):
        money = [startmoney]
        for _ in range(int(T)):
            money.append(money[-1] * (1 + random.normalvariate(mean, sd)))
        finalmoney.append(money[-1])
        last_money_path = money  # Save the last simulation path
    return np.array(finalmoney), last_money_path

def plot_sample_path(money, startmoney):
    fig, ax = plt.subplots()
    ax.plot(money, color='royalblue')
    ax.axhline(y=startmoney, linestyle='--', color='black', label='Starting Money')
    ax.set_xlabel("Months")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    return fig

def plot_final_distribution(finalmoney, startmoney):
    fig, ax = plt.subplots(figsize=(8,5), dpi=150)
    ax.hist(finalmoney, bins=30, color='skyblue', edgecolor='black')
    ax.axvline(startmoney, linestyle='--', color='black', label='Starting Money')
    ax.set_xlabel("Final Money ($)")
    ax.set_ylabel("Frequency")
    ax.legend()
    return fig

def summarize_statistics(finalmoney):
    summary = pd.DataFrame({
        "Mean Final Amount": [finalmoney.mean()],
        "Median Final Amount": [np.median(finalmoney)],
        "Standard Deviation": [finalmoney.std()],
        "Minimum": [finalmoney.min()],
        "Maximum": [finalmoney.max()]
    }).T.rename(columns={0: 'Value'})
    return summary

# --- Streamlit page config and title ---

st.set_page_config(page_title="Investment Simulation", layout="wide")
st.title("Investment Growth Simulation")

# --- Sidebar Inputs ---

st.sidebar.header("Simulation Settings")

mean = st.sidebar.number_input("Expected Monthly Return (%)", value=3.78, step=0.01) / 100
sd = st.sidebar.number_input("Monthly Volatility (%)", value=7.61, step=0.01) / 100
startmoney = st.sidebar.number_input("Starting Money ($)", value=10000, step=100)
T = st.sidebar.number_input("Months", value=12, step=1)
nsim = st.sidebar.number_input("Number of Simulations", value=1000, step=100)

# --- Main Execution ---

if st.sidebar.button("Run Simulation"):
    
    finalmoney, money_path = simulate_investment(mean, sd, startmoney, T, nsim)

    st.subheader("Sample Investment Path (Last Simulation)")
    st.pyplot(plot_sample_path(money_path, startmoney))

    st.subheader(f"Distribution of Final Amounts after {int(T)} Months")
    st.pyplot(plot_final_distribution(finalmoney, startmoney))

    st.subheader("Summary Statistics")
    st.write(summarize_statistics(finalmoney))

else:
    st.info("👈 Adjust settings in the sidebar and click 'Run Simulation'!")

