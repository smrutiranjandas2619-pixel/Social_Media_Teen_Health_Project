import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_feature_importance(model, X_test):

    if not hasattr(model, "feature_importances_"):

        print("This model does not support feature importance.")
        return

    importance_df = pd.DataFrame({
        "Feature": X_test.columns,
        "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    os.makedirs("reports/figures", exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    plt.title("Feature Importance")
    plt.xlabel("Importance")

    plt.gca().invert_yaxis()

    plt.savefig(
        "reports/figures/feature_importance.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(importance_df)