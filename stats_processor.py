import streamlit as st

class StatsProcessor:
    def __init__(self, players_df):
        self.players_df = players_df

    def get_numeric_stats_columns(self):
        return self.players_df.select_dtypes(include=['number']).columns.tolist()

    def normalize(self, series):
        min_val = self.players_df[series.name].min()
        max_val = self.players_df[series.name].max()
        if max_val == min_val:
            return series
        return (series - min_val) / (max_val - min_val)

    def get_normalized_stats(self, player_data, stat_cols):
        stats = player_data[stat_cols]
        return self.normalize(stats)
