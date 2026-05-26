import pandas as pd


def load_dataset(filepath):

    df = pd.read_csv(filepath)

    print("\nDataset Loaded Successfully")

    return df


def dataset_summary(df):

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Info:")
    print(df.info())

    print("\nStatistical Summary:")
    print(df.describe(include='all'))