import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# ============
# PATH SETUP
# ============

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "modeling_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ============
# LOAD DATA
# ============

def load_data():
    return pd.read_csv(DATA_PATH)


# ============================
# PREPARE FEATURES & TARGETS
# ============================

def prepare_data(df):
    X = df.drop(columns=["is_churned", "will_purchase"])
    y_churn = df["is_churned"]
    y_purchase = df["will_purchase"]
    return X, y_churn, y_purchase


# ==================
# TRAIN-TEST SPLIT
# ==================

def split_data(X, y_churn, y_purchase):
    X_train, X_test, y_train_churn, y_test_churn = train_test_split(
        X, y_churn, test_size=0.2, random_state=42
    )

    y_train_purchase = y_purchase.loc[X_train.index]
    y_test_purchase = y_purchase.loc[X_test.index]

    return X_train, X_test, y_train_churn, y_test_churn, y_train_purchase, y_test_purchase


# ===========
# ENCODING
# ===========

def encode_features(X_train, X_test):
    categorical_cols = [
        "customer_segment",
        "engagement_segment",
        "location",
        "acquisition_channel",
        "gender"
    ]

    X_train_encoded = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)
    X_test_encoded = pd.get_dummies(X_test, columns=categorical_cols, drop_first=True)

    X_train_encoded, X_test_encoded = X_train_encoded.align(
        X_test_encoded,
        join="left",
        axis=1,
        fill_value=0
    )

    return X_train_encoded, X_test_encoded


# ===================
# TRAIN CHURN MODEL
# ===================

def train_churn_model(X_train_encoded, y_train_churn):
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train_encoded)

    churn_model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    churn_model.fit(X_train_scaled, y_train_churn)

    return churn_model, scaler


# ======================
# TRAIN PURCHASE MODEL
# ======================

def train_purchase_model(X_train_encoded, y_train_purchase):
    purchase_drop_cols = [
        "frequency",
        "monetary",
        "avg_order_value",
        "purchase_frequency_rate",
        "interaction_purchase_ratio",
        "engaged_not_purchased"
    ]

    X_train_purchase = X_train_encoded.drop(columns=purchase_drop_cols)

    scaler = StandardScaler()
    X_train_purchase_scaled = scaler.fit_transform(X_train_purchase)

    purchase_model = LogisticRegression(max_iter=1000)
    purchase_model.fit(X_train_purchase_scaled, y_train_purchase)

    return purchase_model, scaler, purchase_drop_cols


# ==============
# SAVE MODELS
# ==============

def save_models(churn_model, churn_scaler, purchase_model, purchase_scaler, purchase_drop_cols):
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(churn_model, os.path.join(MODEL_DIR, "churn_model.joblib"))
    joblib.dump(churn_scaler, os.path.join(MODEL_DIR, "churn_scaler.joblib"))

    joblib.dump(purchase_model, os.path.join(MODEL_DIR, "purchase_model.joblib"))
    joblib.dump(purchase_scaler, os.path.join(MODEL_DIR, "purchase_scaler.joblib"))

    joblib.dump(purchase_drop_cols, os.path.join(MODEL_DIR, "purchase_drop_cols.joblib"))


# ================
# MAIN PIPELINE
# ================

def main():
    df = load_data()

    X, y_churn, y_purchase = prepare_data(df)

    X_train, X_test, y_train_churn, y_test_churn, y_train_purchase, y_test_purchase = split_data(
        X, y_churn, y_purchase
    )

    X_train_encoded, X_test_encoded = encode_features(X_train, X_test)

    churn_model, churn_scaler = train_churn_model(X_train_encoded, y_train_churn)

    purchase_model, purchase_scaler, purchase_drop_cols = train_purchase_model(
        X_train_encoded, y_train_purchase
    )

    save_models(
        churn_model,
        churn_scaler,
        purchase_model,
        purchase_scaler,
        purchase_drop_cols
    )


if __name__ == "__main__":
    main()
