import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# --- Helper function to plot radar chart ---
def plot_radar_chart(player_stats, player_names, stats_labels):
    num_vars = len(stats_labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i, player in enumerate(player_names):
        values = player_stats[i].tolist()
        values += values[:1]
        ax.plot(angles, values, label=player)
        ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats_labels)
    ax.set_yticklabels([])
    ax.set_title("Player Comparison Radar Chart")
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    st.pyplot(fig)

# --- Load datasets.csv ---
@st.cache_data
def load_datasets():
    df = pd.read_csv("datasets.csv", delimiter=';')
    return df

datasets_df = load_datasets()

st.title("🎈 Player Comparison App")

# --- Year selection ---
years = ["24-25"]  # Extracted from dataset names for now
year = st.selectbox("Select year:", years)

# --- League selection ---
leagues = datasets_df["LEAGUE"].unique()
league = st.selectbox("Select league:", leagues)

# Load selected league dataset Excel file
dataset_row = datasets_df[datasets_df["LEAGUE"] == league].iloc[0]
file_path = dataset_row["PATH"]
full_path = os.path.join("datasets", file_path)  # Adjust if needed

@st.cache_data
def load_player_data(path):
    # Load Excel file with players data
    df = pd.read_excel(path)
    return df

try:
    players_df = load_player_data(full_path)
except Exception as e:
    st.error(f"Failed to load data file: {e}")
    st.stop()

# Show some info about data
st.write(f"Loaded dataset for **{league}** with {len(players_df)} players.")

# --- Player selection ---
player_names = players_df['Player'].unique()
player1 = st.selectbox("Select Player 1", player_names)
player2 = st.selectbox("Select Player 2", player_names, index=1 if len(player_names) > 1 else 0)

if player1 == player2:
    st.warning("Please select two different players to compare.")
    st.stop()

# --- Filter data for selected players ---
player1_data = players_df[players_df['Player'] == player1].iloc[0]
player2_data = players_df[players_df['Player'] == player2].iloc[0]

# --- Select stats columns to compare (exclude non-numeric and 'Player' column) ---
numeric_cols = players_df.select_dtypes(include=['number']).columns.tolist()
if not numeric_cols:
    st.error("No numeric stats columns found in the dataset to compare.")
    st.stop()

stats_labels = numeric_cols

player1_stats = player1_data[numeric_cols]
player2_stats = player2_data[numeric_cols]

# Normalize stats for radar chart between 0 and 1 for fair comparison
def normalize_series(s):
    min_val = players_df[s.name].min()
    max_val = players_df[s.name].max()
    if max_val == min_val:
        return s  # avoid div by zero
    return (s - min_val) / (max_val - min_val)

player1_stats_norm = normalize_series(player1_stats)
player2_stats_norm = normalize_series(player2_stats)

# Plot radar chart
plot_radar_chart(
    [player1_stats_norm, player2_stats_norm],
    [player1, player2],
    stats_labels
)
