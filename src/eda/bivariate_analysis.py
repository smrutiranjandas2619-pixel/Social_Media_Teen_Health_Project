import seaborn as sns
import matplotlib.pyplot as plt
import os

def correlation_heatmap(df):

    # FULL ABSOLUTE SAVE PATH
    save_path = r"C:\Users\Acer\OneDrive\Desktop\Social_Media_Teen_Health_Project\reports\figures\correlation_heatmap.png"

    # create folder if missing
    os.makedirs(
        os.path.dirname(save_path),
        exist_ok=True
    )

    plt.figure(figsize=(12,8))

    corr = df.corr(numeric_only=True)

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Correlation Heatmap")

    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches='tight'
    )

    print("Saved to:")
    print(save_path)

    plt.close()