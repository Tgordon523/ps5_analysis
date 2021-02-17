### Script to clean and format data
### import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import pathlib
from bs4 import BeautifulSoup


def dataset_clean(path: str) -> pd.DataFrame():
    """
    Function to load and save data regarding ps5 availability history

    Arguments:
        path: path to data source - str
    """
    ### Load dataset
    df = pd.read_csv(path)

    ### Extract price and date
    df["Price"] = df["Status"].str.findall("\d+\.\d+")
    df = df.explode("Price")
    df["Price"] = pd.to_numeric(df["Price"])
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    df["Date"] = df["Date/Time"].dt.date

    ### Extract website and what type of console from data
    df = df.join(
        df.Status.str.split(" - ", expand=True).rename(columns={0: "Site", 1: "Type"})
    )
    df["Edition"] = [x[0].strip() for x in df.Type.str.split("(Out|In)")]

    df = df.sort_values(by=["Date/Time", "Site"], ascending=[False, False])

    df_match = df.join(
        df[["Site", "Type", "Edition", "Date/Time"]].shift(1),
        lsuffix="_Start",
        rsuffix="_End",
    )
    df_match = df_match[
        (df_match["Site_Start"] == df_match["Site_End"])
        & (df_match["Edition_Start"] == df_match["Edition_End"])
    ]

    return df_match


if __name__ == "__main__":
    path = (
        pathlib.Path(r"C:\Users\tgord\MyPyScripts\PS5_EDA")
        / "ps5_analysis"
        / "data"
        / "dataset_raw.csv"
    )
    data = dataset_clean(path)
    data.to_csv(path.parent / "dataset_clean.csv", index=False)
