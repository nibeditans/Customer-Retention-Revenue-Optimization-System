import pandas as pd
import os
import joblib

# =============
# PATH SETUP
# =============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "modeling_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "scoring_output.csv")

# ===========
# LOAD DATA
# ===========
df = pd.read_csv(DATA_PATH)

# =========================
# LOAD MODELS & ARTIFACTS
# =========================
churn_model = joblib.load(os.path.join(MODEL_PATH, "churn_model.joblib"))
purchase_model = joblib.load(os.path.join(MODEL_PATH, "purchase_model.joblib"))

churn_scaler = joblib.load(os.path.join(MODEL_PATH, "churn_scaler.joblib"))
purchase_scaler = joblib.load(os.path.join(MODEL_PATH, "purchase_scaler.joblib"))

purchase_drop_cols = joblib.load(os.path.join(MODEL_PATH, "purchase_drop_cols.joblib"))

# =====================
# FEATURE PREPARATION
# =====================
X = df.drop(columns=["is_churned", "will_purchase"])

categorical_cols = X.select_dtypes(include=["object"]).columns
X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

# ==================
# CHURN PREDICTION
# ==================
churn_features = churn_scaler.feature_names_in_

for col in churn_features:
    if col not in X_encoded.columns:
        X_encoded[col] = 0

X_churn = X_encoded[churn_features]
X_churn_scaled = churn_scaler.transform(X_churn)

df["churn_prob"] = churn_model.predict_proba(X_churn_scaled)[:, 1]

# =====================
# PURCHASE PREDICTION
# =====================
purchase_features = purchase_scaler.feature_names_in_

for col in purchase_features:
    if col not in X_encoded.columns:
        X_encoded[col] = 0

X_purchase = X_encoded[purchase_features]
X_purchase_scaled = purchase_scaler.transform(X_purchase)

df["purchase_prob"] = purchase_model.predict_proba(X_purchase_scaled)[:, 1]

# ===============
# SCORING LOGIC
# ===============
df["expected_revenue"] = df["purchase_prob"] * df["avg_order_value"]
df["adjusted_revenue"] = df["expected_revenue"] * (1 - df["churn_prob"])
df["final_score"] = df["adjusted_revenue"]

# ===================
# BUDGET CONSTRAINT
# ===================
cost_per_customer = 50
budget = 50000
max_customers = int(budget / cost_per_customer)

df = df.sort_values(by="final_score", ascending=False).reset_index(drop=True)

df["selected"] = 0
df.loc[:max_customers - 1, "selected"] = 1

# =================
# BUSINESS IMPACT
# =================
target_df = df[df["selected"] == 1]

uplift_factor = 0.1

incremental_revenue = (
    target_df["purchase_prob"] *
    target_df["avg_order_value"] *
    uplift_factor
)

total_expected_revenue = incremental_revenue.sum()
total_cost = target_df.shape[0] * cost_per_customer
net_profit = total_expected_revenue - total_cost

# =============
# SAVE OUTPUT
# =============
output_df = df[[
    "final_score",
    "churn_prob",
    "purchase_prob",
    "expected_revenue",
    "selected"
]]

output_df.to_csv(OUTPUT_PATH, index=False)

# ===============
# PRINT SUMMARY
# ===============
print("=== OPTIMIZATION SUMMARY ===")
print(f"Total Target Customers: {target_df.shape[0]}")
print(f"Incremental Revenue: ₹ {round(total_expected_revenue, 2)}")
print(f"Campaign Cost: ₹ {total_cost}")
print(f"Net Profit: ₹ {round(net_profit, 2)}")
print("Scoring output saved successfully!")
