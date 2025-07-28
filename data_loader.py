# data_loader.py
import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_datasets_csv(path="datasets.csv"):
    return pd.read_csv(path, delimiter=';')

@st.cache_data
def load_player_data(path):
    return pd.read_excel(path)

class DatasetLoader:
    def __init__(self):
        self.datasets_df = load_datasets_csv()

    def get_leagues(self):
        return self.datasets_df["LEAGUE"].unique()

    def get_dataset_path(self, league):
        row = self.datasets_df[self.datasets_df["LEAGUE"] == league].iloc[0]
        return os.path.join("datasets", row["PATH"])