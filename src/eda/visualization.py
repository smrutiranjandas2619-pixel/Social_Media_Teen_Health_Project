import matplotlib.pyplot as plt
import seaborn as sns


def boxplot_visualization(
        df,
        column
):

    plt.figure(figsize=(7,4))

    sns.boxplot(
        x=df[column]
    )

    plt.title(
        f"Boxplot — {column}"
    )

    plt.show()