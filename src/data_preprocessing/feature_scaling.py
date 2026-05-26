from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import os


def scale_features(df):

    scaler = StandardScaler()

    numerical_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # EXCLUDE TARGET COLUMN
    exclude_cols = [

        'depression_label'

    ]

    numerical_cols = [

        col for col in numerical_cols

        if col not in exclude_cols
    ]

    df[numerical_cols] = scaler.fit_transform(

        df[numerical_cols]
    )

    os.makedirs(
        "models/scalers",
        exist_ok=True
    )

    joblib.dump(

        scaler,

        "models/scalers/standard_scaler.pkl"
    )

    print(
        "Feature scaling completed."
    )

    return df