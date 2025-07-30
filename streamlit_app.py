import streamlit as st
import pandas as pd
from data_loader import DatasetLoader, load_player_data
from stats_processor import StatsProcessor
from chart_plotter import RadarChartPlotter
from enums import Position, Stats

class PlayerComparisonApp:
    def __init__(self):
        self.dataset_loader = DatasetLoader()

    def get_color(self, percent):
        if percent >= 70:
            return "green"
        elif percent >= 40:
            return "yellow"
        elif percent >= 20:
            return "orange"
        else:
            return "red"

    def run(self):
        st.title("Player Comparison App")

        st.sidebar.header("Filter Options")

        # Load dataset metadata
        dataset_metadata = self.dataset_loader.get_metadata()
        available_years = self.dataset_loader.get_years()

        # Player 1 filters
        st.sidebar.subheader("Player 1 Filters")
        year1 = st.sidebar.selectbox("Select year (Player 1):", available_years, key="year1")
        leagues1 = dataset_metadata[dataset_metadata['YEAR'] == year1]['LEAGUE'].unique()
        league1 = st.sidebar.selectbox("Select league (Player 1):", leagues1, key="league1")
        dataset_path1 = self.dataset_loader.get_dataset_path(league1, year1)
        players_df1 = load_player_data(dataset_path1)
        
        # Initialize StatsProcessor for player 1 data and create new columns
        stats_processor1 = StatsProcessor(players_df1)
        stats_processor1.create_columns()
        
        # Select player names from the processed DataFrame to include new columns
        player_names1 = stats_processor1.players_df['Player'].unique()
        player1_name = st.sidebar.selectbox("Select player 1:", player_names1, key="player1")

        st.sidebar.markdown("---")

        # Toggle comparison
        compare_two_players = st.sidebar.checkbox("Compare with a second player", value=True)

        if compare_two_players:
            st.sidebar.subheader("Player 2 Filters")
            year2 = st.sidebar.selectbox("Select year (Player 2):", available_years, key="year2")
            leagues2 = dataset_metadata[dataset_metadata['YEAR'] == year2]['LEAGUE'].unique()
            league2 = st.sidebar.selectbox("Select league (Player 2):", leagues2, key="league2")
            dataset_path2 = self.dataset_loader.get_dataset_path(league2, year2)
            players_df2 = load_player_data(dataset_path2)
            
            stats_processor2 = StatsProcessor(players_df2)
            stats_processor2.create_columns()
            
            player_names2 = stats_processor2.players_df['Player'].unique()
            player2_name = st.sidebar.selectbox("Select player 2:", player_names2, key="player2")

        st.sidebar.markdown("---")

        # === Configuration Selector ===
        config_options = [config.name.replace("_", " ").title() for config in Stats]
        config_options.append("Custom")

        selected_config = st.sidebar.selectbox("Select role configuration:", config_options)

        # === Stat Selection ===
        numeric_cols = stats_processor1.get_numeric_stats_columns()

        if selected_config == "Custom":
            selected_stats = st.sidebar.multiselect(
                "Select stats to compare:",
                options=numeric_cols,
                default=[]
            )
        else:
            config_key = selected_config.upper().replace(" ", "_")
            stats_enum = Stats[config_key]
            default_stats = [s for s in stats_enum.value if s in numeric_cols]
            selected_stats = default_stats

            st.sidebar.markdown(f"**Using predefined stats for:** {selected_config}")
            st.sidebar.write(f"{', '.join(default_stats)}")

        # Validation
        if not selected_stats:
            st.info("Please select at least one stat to proceed.")
            return

        # Select player1_data from stats_processor1's processed DataFrame
        player1_data = stats_processor1.players_df[stats_processor1.players_df['Player'] == player1_name].iloc[0]
        player1_stats_norm = stats_processor1.get_normalized_stats(player1_data, selected_stats)

        if compare_two_players:
            # Prepare both datasets
            stats_processor1.players_df["Year"] = year1
            stats_processor1.players_df["League"] = league1
            stats_processor2.players_df["Year"] = year2
            stats_processor2.players_df["League"] = league2

            stats_processor1.players_df["name_year"] = stats_processor1.players_df["Player"] + f" ({year1})"
            stats_processor2.players_df["name_year"] = stats_processor2.players_df["Player"] + f" ({year2})"

            player1_name_year = f"{player1_name} ({year1})"
            player2_name_year = f"{player2_name} ({year2})"

            if year1 == year2 and league1 == league2:
                # Use one DataFrame and processor for both players
                stats_processor = StatsProcessor(stats_processor1.players_df)
                stats_processor.create_columns()

                player1_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player1_name_year].iloc[0]
                player2_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player2_name_year].iloc[0]

            else:
                # Combine processed DataFrames from both processors
                combined_df = pd.concat([stats_processor1.players_df, stats_processor2.players_df], ignore_index=True)
                stats_processor = StatsProcessor(combined_df)
                stats_processor.create_columns()

                player1_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player1_name_year].iloc[0]
                player2_data = stats_processor.players_df[stats_processor.players_df["name_year"] == player2_name_year].iloc[0]

            player1_stats_norm = stats_processor.get_normalized_stats(player1_data, selected_stats)
            player2_stats_norm = stats_processor.get_normalized_stats(player2_data, selected_stats)

            player1_stats_real = player1_data[selected_stats]
            player2_stats_real = player2_data[selected_stats]

            RadarChartPlotter.plot(
                [player1_stats_norm, player2_stats_norm],
                [player1_stats_real, player2_stats_real],
                [player1_name_year, player2_name_year],
                selected_stats
            )

        else:
            st.header(f"🔎 {player1_name} – Attribute Overview")
            for stat in selected_stats:
                raw_value = player1_data[stat]
                norm_value = player1_stats_norm[stat] * 100
                color = self.get_color(norm_value)

                st.markdown(f"**{stat}**: {raw_value} ({norm_value:.0f}%)")
                st.markdown(f"""
                    <div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden; height: 20px; width: 100%; margin-bottom: 10px;">
                        <div style="width: {norm_value}%; background-color: {color}; height: 100%; text-align: center;">
                            <span style="color: black; font-size: 14px;">{norm_value:.0f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)




if __name__ == "__main__":
    app = PlayerComparisonApp()
    app.run()