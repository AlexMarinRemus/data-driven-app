# data_loader.py
import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_datasets_csv(path="datasets.xlsx"):
    return pd.read_csv(path, delimiter=';')

@st.cache_data
def load_player_data(path):
    return pd.read_excel(path)

class DatasetLoader:
    def __init__(self):
        self.datasets_df = load_datasets_csv()

    def get_leagues(self):
        return self.datasets_df["LEAGUE"].dropna().tolist()

    def get_dataset_path(self, league):
        row = self.datasets_df[self.datasets_df["LEAGUE"] == league]
        if row.empty:
            raise ValueError(f"No dataset path found for league '{league}'")

        path_value = row.iloc[0]["PATH"]
        if not isinstance(path_value, str):
            raise TypeError(f"Expected string for path, got {type(path_value)}: {path_value}")

        return os.path.join("datasets", path_value.strip())