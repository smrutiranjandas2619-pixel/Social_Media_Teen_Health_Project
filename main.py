# ==========================================
# SOCIAL MEDIA TEEN HEALTH PROJECT
# COMPLETE PIPELINE
# ==========================================

import os

# ==========================================
# DATA PREPROCESSING IMPORTS
# ==========================================

from src.data_preprocessing.load_data import *
from src.data_preprocessing.clean_data import *
from src.data_preprocessing.handle_missing import *
from src.data_preprocessing.feature_scaling import *

# ==========================================
# EDA IMPORTS
# ==========================================

from src.eda.univariate_analysis import *
from src.eda.bivariate_analysis import *
from src.eda.multivariate_analysis import *

# ==========================================
# FEATURE ENGINEERING IMPORTS
# ==========================================

from src.feature_engineering.create_features import *
from src.feature_engineering.encoding import *

# ==========================================
# MODEL TRAINING IMPORTS
# ==========================================

from src.models.train_model import *

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "Teen_Mental_Health_Dataset.csv"
)

CLEANED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "cleaned_dataset.csv"
)

PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "engineered_features.csv"
)

# ==========================================
# MAIN PIPELINE
# ==========================================

def main():

    print("\n====================================")
    print("SOCIAL MEDIA TEEN HEALTH AI PROJECT")
    print("====================================")

    # ======================================
    # PHASE 1 — DATA CLEANING & PREPROCESSING
    # ======================================

    print("\nPHASE 1: DATA CLEANING & PREPROCESSING")

    df = load_dataset(
        RAW_DATA_PATH
    )

    dataset_summary(df)

    missing_value_report(df)

    df = remove_duplicates(df)

    df = clean_categorical_columns(df)

    df = fill_missing_values(df)

    df = remove_outliers_iqr(df)

    df = convert_datatypes(df)

    # ======================================
    # PHASE 2 — FEATURE ENGINEERING (ON RAW VALUES)
    # ======================================

    print(
        "\nPHASE 2: FEATURE ENGINEERING"
    )

    df = create_addiction_score(df)

    df = create_sleep_disruption(df)

    df = create_usage_category(df)

    # Save Cleaned & Engineered Raw Dataset for EDA and Dashboard Loading
    os.makedirs(
        os.path.dirname(
            CLEANED_DATA_PATH
        ),
        exist_ok=True
    )

    df.to_csv(
        CLEANED_DATA_PATH,
        index=False
    )

    print(
        "\nCleaned and Engineered Dataset Saved."
    )

    # ======================================
    # PHASE 3 — EXPLORATORY DATA ANALYSIS
    # ======================================

    print(
        "\nPHASE 3: EXPLORATORY DATA ANALYSIS"
    )

    plot_numerical_distribution(df)

    plot_categorical_distribution(df)

    correlation_heatmap(df)

    pairplot_analysis(df)

    print(
        "\nEDA Completed."
    )

    # ======================================
    # PHASE 4 — DATA TRANSFORMATIONS FOR MODELING
    # ======================================

    print(
        "\nPHASE 4: PREPARING FOR MODEL TRAINING"
    )

    df = scale_features(df)

    df = one_hot_encoding(df)

    os.makedirs(
        os.path.dirname(
            PROCESSED_DATA_PATH
        ),
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        "\nProcessed Dataset Saved."
    )

    # ======================================
    # PHASE 5 — MODEL TRAINING
    # ======================================

    print(
        "\nPHASE 5: MODEL TRAINING"
    )

    trained_model = train_models(df)

    print(
        "\nTraining Completed."
    )

    # ======================================
    # PIPELINE FINISHED
    # ======================================

    print("\n====================================")
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("====================================")


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()