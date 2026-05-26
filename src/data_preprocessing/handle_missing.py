import numpy as np


def missing_value_report(df):

    print("\nMissing Values Count:")

    print(df.isnull().sum())

    print("\nMissing Value Percentage:")

    print(
        (df.isnull().sum() / len(df)) * 100
    )


def fill_missing_values(df):

    numerical_cols = df.select_dtypes(
        include=np.number
    ).columns

    categorical_cols = df.select_dtypes(
        include='object'
    ).columns

    for col in numerical_cols:

        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in categorical_cols:

        df[col] = df[col].fillna(
            df[col].mode()[0]
        )

    print("\nMissing values handled.")

    return df