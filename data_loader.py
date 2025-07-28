import pandas as pd
import streamlit as st
import os

# Cache the loading of the Excel file
@st.cache_data
def load_datasets_excel(path="datasets.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.upper()  # Standardize column names
    return df

@st.cache_data
def load_player_data(path):
    return pd.read_excel(path)

class DatasetLoader:
    def __init__(self):
        self.datasets_df = load_datasets_excel()

    def get_years(self):
        return sorted(self.datasets_df["YEAR"].dropna().unique().tolist(), reverse=True)

    def get_leagues_for_year(self, year):
        return self.datasets_df[self.datasets_df["YEAR"] == year]["LEAGUE"].dropna().unique().tolist()

    def get_dataset_path(self, league, year):
        row = self.datasets_df[(self.datasets_df["LEAGUE"] == league) & (self.datasets_df["YEAR"] == year)]
        if row.empty:
            raise ValueError(f"No dataset path found for league '{league}' and year '{year}'")
        
        path_value = row.iloc[0]["PATH"]
        if not isinstance(path_value, str):
            raise TypeError(f"Expected string for path, got {type(path_value)}: {path_value}")

        return os.path.join("datasets", path_value)

    def get_metadata(self):
        return self.datasets_df.copy()