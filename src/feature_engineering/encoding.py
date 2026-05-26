import pandas as pd


def one_hot_encoding(df):

    categorical_cols = df.select_dtypes(
        include=['object','category']
    ).columns

    df = pd.get_dummies(

        df,

        columns=categorical_cols,

        drop_first=True

    )

    print(
        "\nEncoding Completed."
    )

    return df