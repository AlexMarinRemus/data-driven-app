class StatsProcessor:
    def __init__(self, players_df):
        self.players_df = players_df.copy()
        self.players_df.columns = [col.strip() for col in self.players_df.columns]  # <- sanitize

    def get_numeric_stats_columns(self):
        return self.players_df.select_dtypes(include='number').columns.tolist()

    def normalize(self, series):
        column_name = series.name.strip()
        if column_name not in self.players_df.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame columns: {self.players_df.columns.tolist()}")

        min_val = self.players_df[column_name].min()
        max_val = self.players_df[column_name].max()
        if max_val == min_val:
            return series * 0  # avoid division by zero
        return (series - min_val) / (max_val - min_val)

    def get_normalized_stats(self, player_row, columns):
        stats = player_row[columns]
        return self.normalize(stats)
