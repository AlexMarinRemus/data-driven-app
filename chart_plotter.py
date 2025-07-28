import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class RadarChartPlotter:
    @staticmethod
    def plot(stats_list, player_names, categories):
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # complete the loop

        # Close the stats loop for each player
        stats_list = [list(stats) + [stats[0]] for stats in stats_list]

        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

        # Plot each player's stats and fill area
        for stats, name in zip(stats_list, player_names):
            ax.plot(angles, stats, label=name, linewidth=2)
            ax.fill(angles, stats, alpha=0.25)

            # Add stat value labels slightly outside the data point
            for angle, stat in zip(angles, stats):
                ax.text(
                    angle, stat + 0.05, f"{stat:.2f}",
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=9,
                    fontweight='bold'
                )

        # Set category labels — push them out further with the `y` parameter > 1
        ax.set_thetagrids(np.degrees(angles[:-1]), categories, y=1.15)

        # Increase padding between labels and plot
        ax.tick_params(axis='x', pad=20)

        # Set radius limits
        ax.set_ylim(0, 1)

        # Adjust subplot margins to prevent cutting off labels
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.85)

        # Add legend outside the plot to the right
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

        # Remove gridlines if you want, or style them
        ax.grid(True)

        st.pyplot(fig)