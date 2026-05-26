import seaborn as sns
import matplotlib.pyplot as plt
import os


def pairplot_analysis(df):

    # Absolute save path
    save_path = r"C:\Users\Acer\OneDrive\Desktop\Social_Media_Teen_Health_Project\reports\figures\pairplot.png"

    # Create folder if missing
    os.makedirs(
        os.path.dirname(save_path),
        exist_ok=True
    )

    pair = sns.pairplot(df)

    pair.fig.savefig(
        save_path,
        dpi=300,
        bbox_inches='tight'
    )

    print(f"Saved to: {save_path}")

    plt.close()