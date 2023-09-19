import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the poem data after the webscrapping step.

    Parameters
    ----------
    df: pd.DataFrame
        Raw dataframe with 'Unnamed: 0', 'text' and 'info' columns.

    Returns
    -------
    pd.DataFrame
        Clean dataframe, ready to be use for the fine-tuning of our model
    """
    df = df.drop(columns={"Unnamed: 0"})
    df = split_rows_poem(df)
    df = delete_empty_rows(df)
    df = split_column_info(df)
    df = split_column_year(df)
    clean_df = calculate_publication_date(df)
    return clean_df


def split_rows_poem(df: pd.DataFrame) -> pd.DataFrame:
    """
    Separates each verse of a poem. Each line corresponds to a vers in our new dataframe.
    Parameters
    ----------
    df: pd.DataFrame
        Raw dataframe with just a 'text' column.

    Returns
    -------
    pd.DataFrame
        Dataframe with separates vers.
    """
    df = df.assign(text=df.text.str.split("\n")).explode("text")
    df = df.reset_index(drop=True)
    return df


def delete_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Delete the empty rows. Indeed they are many lines without any words.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with a vers in each line but also empty rows.

    Returns
    -------
    pd.DataFrame
        Dataframe with no empty text lines
    """
    j = []
    for i in range(0, len(df)):
        j += [len(df["text"][i])]
    j_indices = []
    for elem in range(len(j)):
        if j[elem] == 0:
            j_indices.append(elem)
    df = df.drop(j_indices)
    df = df.reset_index(drop=True)
    return df


def split_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Separate the information contain in "info" : the author name and the author's life dates

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with a global 'info' column

    Returns
    -------
    pd.DataFrame
        Dataframe with separated informations
    """
    split_column = df["info"].str.split("\n", n=1, expand=True)
    df["author"] = split_column[0]
    df["year"] = split_column[1]
    df.drop(columns=["info"], inplace=True)
    return df


def split_column_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split the author's life date into birth and death

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with just a "year" column containing the author's life date

    Returns
    -------
    pd.DataFrame
        Dataframe with separated columns containing the birth and the death of the author.
    """
    split_column = df["year"].str.split(" - ", n=1, expand=True)
    df["birth"] = split_column[0]
    df["birth"] = df["birth"].astype(int)
    df["death"] = split_column[1]
    df["death"] = df["death"].astype(int)
    df.drop(columns=["year"], inplace=True)
    return df


def calculate_publication_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate an estimated date of publication of the poem, between the 20 yearsof the author and his date of death.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe with two columns : birth and death

    Returns
    -------
    pd.DataFrame
        Dataframe with one column describing the date of publication
    """
    df["twenty"] = df["birth"] + 20
    df["date"] = round((df["twenty"] + df["death"]) / 2, 0)
    df["date"] = df["date"].astype(int)
    df.drop(columns=["birth", "twenty", "death"], inplace=True)
    return df
