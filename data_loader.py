import pandas as pd
import os
import streamlit as st

class DatasetLoader:
    def __init__(self, datasets_csv_path="datasets.csv", datasets_folder="datasets"):
        self.datasets_csv_path = datasets_csv_path
        self.datasets_folder = datasets_folder
        self.datasets_df = self.load_datasets()

    @st.cache_data
    def load_datasets(self):
        return pd.read_csv(self.datasets_csv_path, delimiter=';')

    @st.cache_data
    def load_player_data(self, path):
        return pd.read_excel(path)

    def get_leagues(self):
        return self.datasets_df["LEAGUE"].unique()

    def get_dataset_path(self, league):
        row = self.datasets_df[self.datasets_df["LEAGUE"] == league]
        if row.empty:
            raise ValueError(f"No dataset found for league {league}")
        file_path = row.iloc[0]["PATH"]
        return os.path.join(self.datasets_folder, file_path)
