import pandas as pd
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
features_path = os.path.join(BASE_DIR, "data", "processed", "customer_features.csv")
scoring_path = os.path.join(BASE_DIR, "data", "processed", "scoring_output.csv")

# Load data
features_df = pd.read_csv(features_path)
scoring_df = pd.read_csv(scoring_path)

# Safety check
assert len(features_df) == len(scoring_df), "Row count mismatch!"

# Add customer_id
scoring_df.insert(0, "customer_id", features_df["customer_id"])

# Save back
scoring_df.to_csv(scoring_path, index=False)

print("customer_id added successfully!")
