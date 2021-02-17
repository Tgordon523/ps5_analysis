### Script to pull and update data tracking
### import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import pathlib
from bs4 import BeautifulSoup


def dataset_load() -> pd.DataFrame():
    """
    Function to load and save data regarding ps5 availability history
    """
    ### get site
    url = "https://www.nowinstock.net/videogaming/consoles/sonyps5/full_history.php"

    if isinstance(url, str):
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e.response.text)
    else:
        return None

    if res.status_code == 200:
        r = res.text
        soup = BeautifulSoup(r)
        ### get table and load to df
        table = soup.find_all("table")
        df = pd.read_html(str(table))[0]

    return df


if __name__ == "__main__":
    data_raw = dataset_load()
    save_dataset = (
        pathlib.Path(r"C:\Users\tgord\MyPyScripts\PS5_EDA")
        / "ps5_analysis"
        / "data"
        / "dataset_raw.csv"
    )
    print(save_dataset)
    data_raw.to_csv(
        save_dataset,
        index=False,
    )
