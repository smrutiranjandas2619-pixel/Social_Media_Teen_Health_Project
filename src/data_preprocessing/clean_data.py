import numpy as np


def remove_duplicates(df):

    duplicates = df.duplicated().sum()

    print(f"\nDuplicate Rows: {duplicates}")

    df = df.drop_duplicates()

    return df


def clean_categorical_columns(df):

    categorical_cols = df.select_dtypes(
        include='object'
    ).columns

    for col in categorical_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    print("\nCategorical columns cleaned.")

    return df


def remove_outliers_iqr(df):

    numerical_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if 'depression_label' in numerical_cols:
        numerical_cols.remove('depression_label')

    for col in numerical_cols:

        Q1 = df[col].quantile(0.25)

        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR

        upper = Q3 + 1.5 * IQR

        df = df[
            (df[col] >= lower) &
            (df[col] <= upper)
        ]

    print("\nOutliers removed using IQR.")

    return df


def convert_datatypes(df):

    categorical_cols = df.select_dtypes(
        include='object'
    ).columns

    for col in categorical_cols:

        df[col] = df[col].astype('category')

    print("\nDatatypes converted.")

    return df