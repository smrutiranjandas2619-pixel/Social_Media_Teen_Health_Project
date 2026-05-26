import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.models.classification_models import get_classification_models


def train_models(df):

    target = "depression_label"

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    print("\nTarget Distribution:")
    print(df[target].value_counts())

    if df[target].nunique() < 2:
        raise ValueError(
            "Training stopped: target has only one class. "
            "Check preprocessing and outlier removal."
        )

    non_numeric_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if len(non_numeric_cols) > 0:
        raise ValueError(
            f"Training stopped: non-numeric columns found: {non_numeric_cols}. "
            "Run one_hot_encoding(df) before training."
        )

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    models = get_classification_models()

    best_model = None
    best_model_name = None
    best_score = 0

    for name, model in models.items():

        print(f"\nTraining {name}...")

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        print(f"{name} Accuracy: {accuracy:.4f}")

        if accuracy > best_score:
            best_score = accuracy
            best_model = model
            best_model_name = name

    save_dir = "models/trained_models"

    os.makedirs(save_dir, exist_ok=True)

    joblib.dump(
        best_model,
        os.path.join(save_dir, "best_model.pkl")
    )

    joblib.dump(
        X_test,
        os.path.join(save_dir, "X_test.pkl")
    )

    joblib.dump(
        y_test,
        os.path.join(save_dir, "y_test.pkl")
    )

    print("\nBest Model:", best_model_name)
    print("Best Accuracy:", round(best_score, 4))
    print("Model and test data saved.")

    return best_model