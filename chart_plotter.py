import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(stats_list, player_names, categories):
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Close the stats and angles loop
        stats_list = [list(stats) + [stats[0]] for stats in stats_list]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

        for stats, name in zip(stats_list, player_names):
            ax.plot(angles, stats, label=name)
            ax.fill(angles, stats, alpha=0.25)
            for angle, stat in zip(angles, stats):
                ax.text(angle, stat + 0.05, f"{stat:.2f}", ha='center', va='center')

        # Push labels outward a bit more
        ax.set_thetagrids(np.degrees(angles[:-1]), categories, y=1.12)

        # Add padding for labels so they don’t get cut off
        ax.tick_params(axis='x', pad=15)

        # Adjust subplot margins to avoid clipping labels
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
        fig.tight_layout()

        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))

        st.pyplot(fig)