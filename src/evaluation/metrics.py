from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    roc_auc_score
)


def evaluate_classification_model(model, X_test, y_test):

    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, zero_division=0))
    print("Recall:", recall_score(y_test, y_pred, zero_division=0))
    print("F1 Score:", f1_score(y_test, y_pred, zero_division=0))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    if hasattr(model, "predict_proba"):

        y_prob = model.predict_proba(X_test)[:, 1]

        print("ROC-AUC:", roc_auc_score(y_test, y_prob))