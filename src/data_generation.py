import numpy as np
import pandas as pd

# Reproducibility
np.random.seed(42)

# Date range
START_DATE = "2024-01-01"
END_DATE = "2026-03-31"

start_date = pd.to_datetime(START_DATE)
end_date = pd.to_datetime(END_DATE)

# =========================
# 1. Generate Customers
# =========================
def generate_customers(n_customers):
    
    customer_ids = [f"C{str(i).zfill(5)}" for i in range(1, n_customers + 1)]
    
    # Signup dates (biased slightly toward earlier dates)
    signup_dates = np.random.choice(
        pd.date_range(start_date, end_date - pd.Timedelta(days=90)),
        size=n_customers
    )
    
    # Segments
    segments = np.random.choice(
        ["high", "medium", "low"],
        size=n_customers,
        p=[0.2, 0.5, 0.3]
    )
    
    # Locations
    locations = np.random.choice(
        ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai",
         "Hyderabad", "Pune", "Bhubaneswar", "Ahmedabad", "Jaipur"],
        size=n_customers
    )
    
    # Acquisition channels
    channels = np.random.choice(
        ["organic", "ads", "referral"],
        size=n_customers,
        p=[0.4, 0.4, 0.2]
    )
    
    # Age (18–65)
    ages = np.random.normal(loc=35, scale=10, size=n_customers).astype(int)
    ages = np.clip(ages, 18, 65)
    
    # Gender
    genders = np.random.choice(
        ["male", "female", "other"],
        size=n_customers,
        p=[0.48, 0.48, 0.04]
    )
    
    customers_df = pd.DataFrame({
        "customer_id": customer_ids,
        "signup_date": signup_dates,
        "customer_segment": segments,
        "location": locations,
        "acquisition_channel": channels,
        "age": ages,
        "gender": genders
    })
    
    return customers_df

# =========================
# 2. Generate Products
# =========================
def generate_products(n_products):
    
    product_ids = [f"P{str(i).zfill(4)}" for i in range(1, n_products + 1)]
    
    categories = ["electronics", "clothing", "home", "beauty", "sports"]
    
    # Assign categories (uneven distribution for realism)
    product_categories = np.random.choice(
        categories,
        size=n_products,
        p=[0.25, 0.25, 0.2, 0.15, 0.15]
    )
    
    prices = []
    costs = []
    
    for cat in product_categories:
        
        if cat == "electronics":
            price = np.random.randint(5000, 50000)
        elif cat == "clothing":
            price = np.random.randint(500, 5000)
        elif cat == "home":
            price = np.random.randint(1000, 15000)
        elif cat == "beauty":
            price = np.random.randint(200, 3000)
        else:  # sports
            price = np.random.randint(800, 10000)
        
        # Cost = 60%–80% of price
        cost = price * np.random.uniform(0.6, 0.8)
        
        prices.append(price)
        costs.append(round(cost, 2))
    
    # Launch dates
    launch_dates = np.random.choice(
        pd.date_range(start_date - pd.Timedelta(days=180), end_date),
        size=n_products
    )
    
    products_df = pd.DataFrame({
        "product_id": product_ids,
        "category": product_categories,
        "price": prices,
        "cost": costs,
        "launch_date": launch_dates
    })
    
    return products_df


# =========================
# 3. Generate Interactions
# =========================
def generate_interactions(customers, products, target_interactions=250000):
    
    interaction_data = []
    interaction_id = 1
    
    product_ids = products["product_id"].values
    
    for _, customer in customers.iterrows():
        
        # Stop if target reached
        if len(interaction_data) >= target_interactions:
            break
        
        customer_id = customer["customer_id"]
        segment = customer["customer_segment"]
        signup_date = customer["signup_date"]
        
        current_date = signup_date
        last_active_date = signup_date
        
        churned = False
        
        # Segment-based configs
        if segment == "high":
            monthly_range = (20, 40)
            churn_days = 90
        elif segment == "medium":
            monthly_range = (8, 20)
            churn_days = 60
        else:
            monthly_range = (2, 8)
            churn_days = 30
        
        # Loop over months
        while current_date <= end_date and not churned:
            
            # Stop if target reached
            if len(interaction_data) >= target_interactions:
                break
            
            # Get current month's date range ONCE (performance fix)
            month_start = current_date.replace(day=1)
            month_end = month_start + pd.offsets.MonthEnd(0)
            days_in_month = pd.date_range(month_start, month_end)
            
            # Number of interactions this month
            n_interactions = np.random.randint(monthly_range[0], monthly_range[1] + 1)
            
            for _ in range(n_interactions):
                
                # Stop if target reached
                if len(interaction_data) >= target_interactions:
                    break
                
                # Sample interaction time
                interaction_time = np.random.choice(days_in_month)
                
                # Ensure interaction is AFTER signup_date
                if interaction_time < signup_date:
                    continue
                
                # Interaction type
                interaction_type = np.random.choice(
                    ["view", "click", "add_to_cart", "email_open"],
                    p=[0.5, 0.25, 0.15, 0.1]
                )
                
                # Product association
                if np.random.rand() < 0.7:
                    product_id = np.random.choice(product_ids)
                else:
                    product_id = None
                
                # Channel logic
                if interaction_type == "email_open":
                    channel = "email"
                else:
                    channel = np.random.choice(["web", "app"], p=[0.7, 0.3])
                
                # Append interaction
                interaction_data.append({
                    "interaction_id": interaction_id,
                    "customer_id": customer_id,
                    "interaction_type": interaction_type,
                    "product_id": product_id,
                    "interaction_timestamp": interaction_time,
                    "channel": channel
                })
                
                interaction_id += 1
                last_active_date = interaction_time
            
            # Move to next month
            current_date = current_date + pd.DateOffset(months=1)
            
            # Churn check
            if (current_date - last_active_date).days > churn_days:
                churned = True
    
    interactions_df = pd.DataFrame(interaction_data)
    
    return interactions_df


# =========================
# 4. Generate Transactions
# =========================
def generate_transactions(interactions, customers, products):
    
    transaction_data = []
    transaction_id = 1
    
    # Fast lookup maps
    customer_segment_map = customers.set_index("customer_id")["customer_segment"].to_dict()
    product_price_map = products.set_index("product_id")["price"].to_dict()
    
    for _, interaction in interactions.iterrows():
        
        interaction_type = interaction["interaction_type"]
        customer_id = interaction["customer_id"]
        product_id = interaction["product_id"]
        interaction_time = interaction["interaction_timestamp"]
        
        # Skip if no product associated
        if pd.isna(product_id):
            continue
        
        # Updated (balanced) conversion probabilities
        if interaction_type == "add_to_cart":
            base_prob = 0.35
        elif interaction_type == "click":
            base_prob = 0.15
        elif interaction_type == "view":
            base_prob = 0.05
        else:
            continue  # email_open doesn't convert
        
        # Segment multiplier
        segment = customer_segment_map[customer_id]
        
        if segment == "high":
            multiplier = 1.5
        elif segment == "medium":
            multiplier = 1.0
        else:
            multiplier = 0.5
        
        final_prob = base_prob * multiplier
        
        # Conversion decision
        if np.random.rand() < final_prob:
            
            quantity = np.random.randint(1, 4)
            price = product_price_map[product_id]
            
            # Discount logic
            if np.random.rand() < 0.8:
                discount = np.random.uniform(0, 0.10)
            else:
                discount = np.random.uniform(0.10, 0.30)
            
            transaction_data.append({
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "product_id": product_id,
                "transaction_date": interaction_time,
                "quantity": quantity,
                "price": price,
                "discount": round(discount, 2)
            })
            
            transaction_id += 1
    
    transactions_df = pd.DataFrame(transaction_data)
    
    return transactions_df


# =========================
# 5. Main Pipeline
# =========================
def run_data_generation(n_customers=8000, n_products=120):
    
    customers = generate_customers(n_customers)
    products = generate_products(n_products)
    interactions = generate_interactions(customers, products)
    transactions = generate_transactions(interactions, customers, products)
    
    return customers, products, interactions, transactions

if __name__ == "__main__":
    customers, products, interactions, transactions = run_data_generation()

