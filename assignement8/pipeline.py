import pandas as pd

from assignement8.arxiv_api import fetch_arxiv_to_dataframe
from assignement8.html_downloader import download_html
from assignement8.mariadb_loader import insert_into_mariadb
from assignement8.mongodb_loader import export_to_mongodb
from assignement8.text_extractor import extract_text_from_html


def add_html(df: pd.DataFrame) -> pd.DataFrame:
    df["content"] = df.apply(lambda row: download_html(row), axis=1)
    return df


def add_text(df: pd.DataFrame) -> pd.DataFrame:
    df["content"] = df["content"].apply(extract_text_from_html)
    return df


def run_pipeline(query: str, max_results: int = 10) -> pd.DataFrame:
    df = (
        fetch_arxiv_to_dataframe(query, max_results)
        .pipe(add_html)
        .pipe(add_text)
        .pipe(insert_into_mariadb)
        .pipe(export_to_mongodb)
    )
    return df
