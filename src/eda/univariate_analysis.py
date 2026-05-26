import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

SAVE_DIR = os.path.join(
    BASE_DIR,
    "reports",
    "figures"
)

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)


def plot_numerical_distribution(df):

    numerical_cols = df.select_dtypes(
        include=np.number
    ).columns

    for col in numerical_cols:

        plt.figure(figsize=(8,4))

        sns.histplot(
            df[col],
            kde=True
        )

        plt.title(f"Distribution — {col}")

        save_path = os.path.join(
            SAVE_DIR,
            f"{col}_distribution.png"
        )

        plt.savefig(save_path)

        print(f"Saved: {save_path}")

        plt.close()


def plot_categorical_distribution(df):

    categorical_cols = df.select_dtypes(
        include=['object','category']
    ).columns

    for col in categorical_cols:

        plt.figure(figsize=(8,4))

        sns.countplot(
            data=df,
            x=col
        )

        plt.title(f"Count — {col}")

        plt.xticks(rotation=45)

        save_path = os.path.join(
            SAVE_DIR,
            f"{col}_countplot.png"
        )

        plt.savefig(save_path)

        print(f"Saved: {save_path}")

        plt.close()