import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

# Math part
def calculate_d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    if T <= 0:
        return np.maximum(S - K, 0) if option_type == 'call' else np.maximum(K - S, 0)

    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


# Visualization via Streamlit
st.set_page_config(page_title="Black-Scholes Options Pricing", layout="wide")
st.title("Black-Scholes Pricing Model")

# Parameters
st.sidebar.header("Current Parameters")
S = st.sidebar.number_input("Current Asset Price (S)", value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (Years, T)", value=1.0, min_value=0.01, step=0.01)
sigma = st.sidebar.number_input("Volatility (sigma)", value=0.20, min_value=0.01, step=0.01)
r = st.sidebar.number_input("Risk-Free Interest Rate (r)", value=0.05, step=0.01)

# Heatmap limits
st.sidebar.header("Heatmap Parameters")
min_spot = st.sidebar.number_input("Min Spot Price", value=80.0, step=1.0)
max_spot = st.sidebar.number_input("Max Spot Price", value=120.0, step=1.0)
min_vol = st.sidebar.number_input("Min Volatility (sigma)", value=0.10, min_value=0.01, step=0.01)
max_vol = st.sidebar.number_input("Max Volatility (sigma)", value=0.50, min_value=0.01, step=0.01)


# Current prices
call_price = black_scholes_price(S, K, T, r, sigma, option_type='call')
put_price = black_scholes_price(S, K, T, r, sigma, option_type='put')

st.subheader("Current Option Prices")
col1, col2 = st.columns(2)
col1.metric("Call Price", f"${call_price:.4f}")
col2.metric("Put Price", f"${put_price:.4f}")

st.divider()

# Scenario Analysis: Heatmaps
st.subheader("Scenario Analysis: Options Price Heatmaps")

# Generate arrays for Spot Price and Volatility
spot_range = np.linspace(min_spot, max_spot, 10)
vol_range = np.linspace(min_vol, max_vol, 10)

# Create 2D matrices to hold the calculated prices
call_matrix = np.zeros((len(vol_range), len(spot_range)))
put_matrix = np.zeros((len(vol_range), len(spot_range)))

# Calculate prices for the matrices
for i, vol in enumerate(vol_range):
    for j, spot in enumerate(spot_range):
        call_matrix[i, j] = black_scholes_price(spot, K, T, r, vol, 'call')
        put_matrix[i, j] = black_scholes_price(spot, K, T, r, vol, 'put')

# Format the axes labels
spot_labels = [f"${x:.1f}" for x in spot_range]
vol_labels = [f"{x*100:.1f}%" for x in vol_range]

# Create columns for heatmaps
fig_col1, fig_col2 = st.columns(2)

# Call Heatmap
with fig_col1:
    st.markdown("#### Call Price Heatmap")
    fig_call = go.Figure(data=go.Heatmap(
        z=call_matrix,
        x=spot_labels,
        y=vol_labels,
        colorscale='Viridis',
        text=np.round(call_matrix, 2),
        texttemplate="%{text}",
        hoverinfo="text"
    ))
    fig_call.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white')
    )
    st.plotly_chart(fig_call, use_container_width=True)

# Put Heatmap
with fig_col2:
    st.markdown("#### Put Price Heatmap")
    fig_put = go.Figure(data=go.Heatmap(
        z=put_matrix,
        x=spot_labels,
        y=vol_labels,
        colorscale='Plasma',
        text=np.round(put_matrix, 2),
        texttemplate="%{text}",
        hoverinfo="text"
    ))
    fig_put.update_layout(
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white')
    )
    st.plotly_chart(fig_put, use_container_width=True)