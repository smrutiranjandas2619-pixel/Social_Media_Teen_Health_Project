import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(model, X_test, y_test):

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    os.makedirs("reports/figures", exist_ok=True)

    plt.figure(figsize=(6, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(
        "reports/figures/confusion_matrix.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()