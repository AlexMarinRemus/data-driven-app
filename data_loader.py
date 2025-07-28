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
def load_player_data(path, min_minutes=600):
    df = pd.read_excel(path)
    df.columns = [col.strip() for col in df.columns]

    # Filter by "Minutes played"
    if "Minutes played" in df.columns:
        df = df[df["Minutes played"] > min_minutes]
    else:
        st.warning(f"'Minutes played' column not found in dataset: {path}")

    return df

class DatasetLoader:
    def __init__(self):
        self.datasets_df = load_datasets_excel()

    def get_years(self):
        raw_years = self.datasets_df["YEAR"].dropna().unique()

        cleaned_years = []
        for y in raw_years:
            try:
                cleaned_years.append(int(float(str(y).strip())))
            except Exception as e:
                st.warning(f"Skipping invalid year value: {y} ({e})")

        if not cleaned_years:
            st.error("No valid years found in dataset metadata.")
            return []

        return sorted(set(cleaned_years), reverse=True)


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