import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(stats_list, player_names, categories, figsize=(7, 7)):
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        stats_list = [list(stats) + [stats[0]] for stats in stats_list]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

        for stats, name in zip(stats_list, player_names):
            ax.plot(angles, stats, label=name)
            ax.fill(angles, stats, alpha=0.25)
            for angle, stat in zip(angles, stats):
                ax.text(angle, stat + 0.05, f"{stat:.2f}", ha='center', va='center')

        ax.set_thetagrids(np.degrees(angles[:-1]), categories, y=1.05)
        fig.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.85)

        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

        st.pyplot(fig)