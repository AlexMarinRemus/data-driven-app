import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(stats_list, player_names, categories):
        num_vars = len(categories)

        # Compute angle for each category
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        # Close the plot
        stats_list = [list(stats) + [stats[0]] for stats in stats_list]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for stats, name in zip(stats_list, player_names):
            ax.plot(angles, stats, label=name)
            ax.fill(angles, stats, alpha=0.25)

            # Add data labels for each point
            for angle, stat in zip(angles, stats):
                ax.text(angle, stat + 0.05, f"{stat:.2f}", ha='center', va='center')

        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.set_ylim(0, 1)  # Assuming normalized stats 0-1
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
        plt.show()
