from pathlib import Path

import pandas as pd
from langdetect import detect
from pandarallel import pandarallel
from tqdm import tqdm

tqdm.pandas()
pandarallel.initialize(progress_bar=True)


def clean_export(external_path):
    """clean up export data"""

    # parse claps as integer on read
    export = pd.read_csv(external_path / "export.csv")
    # lowercase column names
    export.columns = export.columns.str.lower()
    # join year month day column into one
    export["date"] = (
        export["year"].astype(str)
        + "-"
        + export["month"].astype(str)
        + "-"
        + export["day"].astype(str)
    )
    # rename reading_time to read_time
    export.rename(columns={"reading_time": "read_time"}, inplace=True)
    # drop subtitle, image, and year month day columns, and comment and author url
    export.drop(
        columns=["subtitle", "image", "year", "month", "day", "comment", "author_url"],
        inplace=True,
    )
    # reorder columns
    export = export[["title", "claps", "read_time", "author", "publication", "url", "date", "tag"]]
    # replace _ to - in tag column
    export["tag"] = export["tag"].str.replace("_", "-")

    # convert date to datetime
    export["date"] = pd.to_datetime(export["date"])

    return export


def clean_main(raw_path, interim_path, export_df):
    """clean up scraped data and export data"""

    def detect_lang(title):
        """detect language of title"""
        try:
            return detect(title)
        except Exception:
            return "unknown"

    df = pd.read_csv(raw_path / "medium.csv", parse_dates=["date"])

    # concat dataframes
    df = pd.concat([df, export_df], ignore_index=True)

    df["claps"] = df["claps"].apply(
        lambda x: int(float(x.replace("K", "")) * 1000) if "K" in x else int(x)
    )

    # Remove duplicates
    df = df.drop_duplicates(subset=["title"])

    # reset index
    df.reset_index(drop=True, inplace=True)

    # drop missing titles
    df = df.dropna(subset=["title"])
    df = df[df["title"] != " "]

    # filter english
    df = df[df["title"].parallel_apply(lambda x: detect_lang(x) == "en")]

    # dump clean df to interim folder
    df.to_parquet(interim_path / "clean_df.parquet", index=False)


def final_df(interim_path, final_path):

    df = pd.read_parquet(interim_path / "clean_df.parquet")

    # filter title and claps column
    df = df[["title", "claps"]]

    # filter length of title between 30 and 70 characters
    df = df[df["title"].str.len().between(30, 70)]

    # remove titles with "->" to avoid confusion with the prompt
    df = df[~df["title"].str.contains("->")]

    # filter claps >= 10
    df = df[df["claps"] >= 10]

    # dump final df to final folder
    df.to_csv(final_path / "final_df.csv", index=False)


def main():

    # set paths
    project_dir = Path(__file__).resolve().parents[2]
    data_path = project_dir / "data"

    external_path = data_path / "0_external"
    raw_path = data_path / "0_raw"
    interim_path = data_path / "1_interim"
    final_path = data_path / "2_final"

    # clean export data
    export_df = clean_export(external_path)

    # clean main data
    clean_main(raw_path, interim_path, export_df)

    # create final df
    final_df(interim_path, final_path)


if __name__ == "__main__":
    main()
