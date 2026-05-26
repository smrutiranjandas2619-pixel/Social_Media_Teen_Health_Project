from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


def get_classification_models():

    models = {

        "Logistic Regression":
        LogisticRegression(

            class_weight='balanced',

            max_iter=1000
        ),

        "Random Forest":
        RandomForestClassifier(

            n_estimators=100,

            class_weight='balanced',

            random_state=42
        ),

        "SVM":
        SVC(

            class_weight='balanced'
        )
    }

    return models