import streamlit as st

from data_loader import DatasetLoader, load_player_data
from player_selector import PlayerSelector
from stats_processor import StatsProcessor
from chart_plotter import RadarChartPlotter

class PlayerComparisonApp:
    def __init__(self):
        self.dataset_loader = DatasetLoader()

    def run(self):
        st.title("🎈 Player Comparison App")

        # Create two columns: left for all filters, right for chart
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.header("Player 1 Filters")
            years = ["24-25"]
            year1 = st.selectbox("Select year (Player 1):", years, key="year1")

            leagues1 = self.dataset_loader.get_leagues()
            league1 = st.selectbox("Select league (Player 1):", leagues1, key="league1")

            dataset_path1 = self.dataset_loader.get_dataset_path(league1)
            players_df1 = load_player_data(dataset_path1)

            player_names1 = players_df1['Player'].unique()
            player1_name = st.selectbox("Select player 1:", player_names1, key="player1")

        with col2:
            st.header("Player 2 Filters")
            year2 = st.selectbox("Select year (Player 2):", years, key="year2")

            leagues2 = self.dataset_loader.get_leagues()
            league2 = st.selectbox("Select league (Player 2):", leagues2, key="league2")

            dataset_path2 = self.dataset_loader.get_dataset_path(league2)
            players_df2 = load_player_data(dataset_path2)

            player_names2 = players_df2['Player'].unique()
            player2_name = st.selectbox("Select player 2:", player_names2, key="player2")

        # Stats multiselect spanning first two columns — use st.columns with 2 equal widths here
        cols = st.columns(2)
        stats_processor1 = StatsProcessor(players_df1)
        numeric_cols = stats_processor1.get_numeric_stats_columns()

        with cols[0]:
            selected_stats = st.multiselect(
                "Select stats to compare:",
                options=numeric_cols,
                default=["Goals", "Assists", "xG"] if set(["Goals", "Assists", "xG"]).issubset(numeric_cols) else []
            )

        # Plot in the 3rd column
        with col3:
            if selected_stats:
                player1_data = players_df1[players_df1['Player'] == player1_name].iloc[0]
                player2_data = players_df2[players_df2['Player'] == player2_name].iloc[0]

                player1_stats_norm = stats_processor1.get_normalized_stats(player1_data, selected_stats)
                stats_processor2 = StatsProcessor(players_df2)
                player2_stats_norm = stats_processor2.get_normalized_stats(player2_data, selected_stats)

                RadarChartPlotter.plot(
                    [player1_stats_norm, player2_stats_norm],
                    [player1_name, player2_name],
                    selected_stats,
                    figsize=(15, 15)
                )
            else:
                st.info("Please select at least one stat to display the radar chart.")



if __name__ == "__main__":
    app = PlayerComparisonApp()
    app.run()
