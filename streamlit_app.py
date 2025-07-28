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
        col1, col2 = st.columns([1, 3])

        with col1:
            years = ["24-25"]
            year = st.selectbox("Select year:", years)

            leagues = self.dataset_loader.get_leagues()
            league = st.selectbox("Select league:", leagues)

            dataset_path = self.dataset_loader.get_dataset_path(league)
            try:
                players_df = load_player_data(dataset_path)
            except Exception as e:
                st.error(f"Failed to load data file: {e}")
                st.stop()

            st.write(f"Loaded dataset for **{league}** with {len(players_df)} players.")

            player_selector = PlayerSelector(players_df)
            player1_name, player2_name = player_selector.select_players()

            numeric_cols = StatsProcessor(players_df).get_numeric_stats_columns()

            default_stats = ['Goals', 'Assists', 'xG']
            selected_stats = st.multiselect(
                "Select stats to compare:",
                options=numeric_cols,
                default=[s for s in default_stats if s in numeric_cols]
            )

            if not selected_stats:
                st.warning("Select at least one stat to show on the chart.")

        with col2:
            if selected_stats:
                player1_data = players_df[players_df['Player'] == player1_name].iloc[0]
                player2_data = players_df[players_df['Player'] == player2_name].iloc[0]

                stats_processor = StatsProcessor(players_df)
                player1_stats_norm = stats_processor.get_normalized_stats(player1_data, selected_stats)
                player2_stats_norm = stats_processor.get_normalized_stats(player2_data, selected_stats)

                RadarChartPlotter.plot(
                    [player1_stats_norm, player2_stats_norm],
                    [player1_name, player2_name],
                    selected_stats
                )



if __name__ == "__main__":
    app = PlayerComparisonApp()
    app.run()
