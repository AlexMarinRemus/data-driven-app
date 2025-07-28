import streamlit as st

from data_loader import DatasetLoader
from player_selector import PlayerSelector
from stats_processor import StatsProcessor
from chart_plotter import RadarChartPlotter

class PlayerComparisonApp:
    def __init__(self):
        self.dataset_loader = DatasetLoader()

    def run(self):
        st.title("🎈 Player Comparison App")

        years = ["24-25"]
        year = st.selectbox("Select year:", years)

        leagues = self.dataset_loader.get_leagues()
        league = st.selectbox("Select league:", leagues)

        dataset_path = self.dataset_loader.get_dataset_path(league)
        try:
            players_df = self.dataset_loader.load_player_data(dataset_path)
        except Exception as e:
            st.error(f"Failed to load data file: {e}")
            st.stop()

        st.write(f"Loaded dataset for **{league}** with {len(players_df)} players.")

        player_selector = PlayerSelector(players_df)
        player1_name, player2_name = player_selector.select_players()

        player1_data = players_df[players_df['Player'] == player1_name].iloc[0]
        player2_data = players_df[players_df['Player'] == player2_name].iloc[0]

        stats_processor = StatsProcessor(players_df)
        numeric_cols = stats_processor.get_numeric_stats_columns()
        if not numeric_cols:
            st.error("No numeric stats columns found in the dataset to compare.")
            st.stop()

        player1_stats_norm = stats_processor.get_normalized_stats(player1_data, numeric_cols)
        player2_stats_norm = stats_processor.get_normalized_stats(player2_data, numeric_cols)

        RadarChartPlotter.plot(
            [player1_stats_norm, player2_stats_norm],
            [player1_name, player2_name],
            numeric_cols
        )


if __name__ == "__main__":
    app = PlayerComparisonApp()
    app.run()
