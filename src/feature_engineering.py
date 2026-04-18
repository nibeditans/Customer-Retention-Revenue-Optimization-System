import pandas as pd
from sqlalchemy import create_engine
import os


# Config
engine = create_engine(
    "postgresql://my_username:my_password@localhost:5432/crros_database"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 1. Export Customer Features
def export_customer_features():
    query = "SELECT * FROM customer_features;"
    df = pd.read_sql(query, engine)

    output_path = os.path.join(BASE_DIR, "data", "processed", "customer_features.csv")
    df.to_csv(output_path, index=False)

    print("Customer features saved to:", output_path)


# 2. Create Dashboard Dataset
def create_dashboard_dataset():
    
    # Load data
    features_path = os.path.join(BASE_DIR, "data", "processed", "customer_features.csv")
    scoring_path = os.path.join(BASE_DIR, "data", "processed", "scoring_output.csv")

    features_df = pd.read_csv(features_path)
    scoring_df = pd.read_csv(scoring_path)

    # Merge
    df = scoring_df.merge(
        features_df[
            [
                "customer_id",
                "customer_segment",
                "engagement_segment",
                "age",
                "gender",
                "location",
                "acquisition_channel"
            ]
        ],
        on="customer_id",
        how="left"
    )

    # Output
    output_path = os.path.join(BASE_DIR, "data", "processed", "dashboard_dataset.csv")
    df.to_csv(output_path, index=False)

    print("Dashboard dataset saved to:", output_path)


# Main Execution
if __name__ == "__main__":
    export_customer_features()
    create_dashboard_dataset()
