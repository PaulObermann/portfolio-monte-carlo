import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Investment Simulation", layout="wide")
st.title("Investment Growth Simulation")

# Sidebar for parameters
st.sidebar.header("Simulation Settings")

mean = st.sidebar.number_input("Expected Monthly Return (%)", value=3.78, step=0.01) / 100
sd = st.sidebar.number_input("Monthly Volatility (%)", value=7.61, step=0.01) / 100
startmoney = st.sidebar.number_input("Starting Money ($)", value=10000, step=100)
T = st.sidebar.number_input("Months", value=12, step=1)
nsim = st.sidebar.number_input("Number of Simulations", value=1000, step=100)

# Button to run simulation
if st.sidebar.button("Run Simulation"):
    finalmoney = []

    for _ in range(int(nsim)):
        money = [startmoney]
        for _ in range(int(T)):
            money.append(money[-1]*(1+random.normalvariate(mean, sd)))

        finalmoney.append(money[-1])

    # Plotting last simulation path
    st.subheader("Sample Investment Path (Last Simulation)")
    fig1, ax1 = plt.subplots()
    ax1.plot(money, color='royalblue')
    ax1.axhline(y=startmoney, linestyle='--', color='black', label='Starting Money')
    ax1.set_xlabel("Months")
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.legend()
    st.pyplot(fig1)

    # Histogram of final values
    st.subheader(f"Distribution of Final Amounts after {int(T)} Months")
    fig2, ax2 = plt.subplots(figsize=(8,5), dpi=150)
    ax2.hist(finalmoney, bins=30, color='skyblue', edgecolor='black')
    ax2.axvline(startmoney, linestyle='--', color='black', label='Starting Money')
    ax2.set_xlabel("Final Money ($)")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    st.pyplot(fig2)

    # Statistics
    finalmoney = np.array(finalmoney)
    st.subheader("Summary Statistics")
    st.write(pd.DataFrame({
        "Mean Final Amount": [finalmoney.mean()],
        "Median Final Amount": [np.median(finalmoney)],
        "Standard Deviation": [finalmoney.std()],
        "Minimum": [finalmoney.min()],
        "Maximum": [finalmoney.max()]
    }).rename(columns={'0': 'Value'}).T)

else:
    st.info("👈 Adjust settings in the sidebar and click 'Run Simulation'!")

