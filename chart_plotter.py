import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(player_stats_list, player_names, stats_labels):
        num_vars = len(stats_labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for i, player in enumerate(player_names):
            values = player_stats_list[i].tolist()
            values += values[:1]
            ax.plot(angles, values, label=player)
            ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(stats_labels)
        ax.set_yticklabels([])
        ax.set_title("Player Comparison Radar Chart")
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        st.pyplot(fig)
