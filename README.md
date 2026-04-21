# Customer Retention & Revenue Optimization System

An end-to-end Data Science system designed to predict customer churn, estimate purchase probability, and optimize customer targeting to maximize revenue under budget constraints.


## Problem Statement

Businesses often struggle with inefficient marketing spend because:
- Not all customers contribute equally to revenue  
- Some customers are likely to churn  
- Marketing budgets are limited  

**Goal:**   
Identify the right customers to target in order to **maximize revenue while minimizing waste**.

**Check out the article I have written on this Project:**
- Complete Project Walkthrough: [How to Identify High-Value Customers and Maximize Revenue with Data Science?](https://nsdsda.medium.com/how-to-identify-high-value-customers-and-maximize-revenue-with-data-science-110f77446c6b)


## Solution Overview

This project simulates a real-world business workflow:
1. Understand customer behavior  
2. Predict future actions (churn & purchase)  
3. Optimize customer targeting under budget constraints  
4. Estimate business impact  


## Project Pipeline

> Data Simulation → Database → SQL Analysis → Feature Engineering → Modeling → Optimization → Business Impact


## Data Design

A synthetic but behavior-driven dataset was created with:
- Customer segments (High / Medium / Low value)
- Interaction patterns
- Purchase behavior
- Churn signals
- Noise, missing values, and realistic variability

## Data Engineering

- Data stored and managed using PostgreSQL  
- SQL used for:
  - Data validation  
  - Exploration  
  - Feature engineering (RFM + engagement metrics)

## Feature Engineering

Key features include:
- Recency, Frequency, Monetary (RFM)
- Engagement metrics
- Interaction-to-purchase ratio
- Behavioral segmentation

## Modeling

Two predictive models were built:

### 1. Churn Prediction
- Identifies customers at risk of leaving

### 2. Purchase Probability
- Estimates likelihood of future purchase

Models used:
- Logistic Regression  
- Random Forest  

Focus was on:
- Interpretability  
- Business relevance  

## Optimization Strategy

Customers were ranked based on expected value:
- Combined churn risk and purchase probability  
- Applied budget constraint  
- Selected top 1000 customers for targeting  

## Business Impact

| Metric | Value |
|------|------|
| Total Customers | 8000 |
| Targeted Customers | 1000 |
| Expected Revenue | ₹16.66M |
| Campaign Cost | ₹50K |
| Net Profit | ₹16.61M |

**Insight:**   
A small subset of customers drives the majority of revenue.

## Dashboard

The dashboard focuses on decision-making:
- KPI summary (Revenue, Profit, Targets)
- Customer segment distribution
- Targeting strategy visualization (risk vs opportunity)


## Key Insights

- Customer value is highly uneven  
- Engagement strongly drives purchase behavior  
- Inactivity is a strong indicator of churn  
- Targeting high-value customers significantly improves efficiency

----

## 🤖 AI-Powered Business Insights Layer

### Overview

To bridge the gap between model outputs and business decision-making, I integrated a lightweight AI layer into the pipeline.

While the system generates predictions (churn probability, purchase likelihood, expected revenue), business stakeholders need **clear, actionable insights**, not raw numbers.

This layer translates structured model outputs into:

* Key observations
* Business interpretation
* Actionable recommendations

### Approach

Instead of passing raw data, the system feeds **curated business metrics** into an LLM, including:

* Customer segment churn rates
* Targeting strategy metrics (purchase & churn probabilities)
* Campaign performance (revenue, cost, profit)

A **multi-model fallback mechanism** is implemented using OpenRouter to improve reliability. If all models fail (common with free endpoints), the system switches to a **deterministic fallback insight generator**.

This ensures:

* Robustness
* Consistent output
* No dependency on external API availability

### Sample AI-Generated Insight

> **Key Observations**
>
> * Low-value customers exhibit the highest churn (~21%)
> * High-value customers are relatively more stable (~18%)
> * Targeted customers show very high purchase probability (~94%)

> **Business Interpretation**
>
> * The targeting strategy prioritizes **high conversion likelihood** rather than churn prevention
> * This reflects a **revenue maximization approach**

> **Recommended Actions**
>
> * Continue targeting high purchase probability customers
> * Design separate retention campaigns for high-churn segments
> * Monitor long-term churn impact to balance growth and retention


### Why This Matters?

Traditional ML pipelines stop at predictions. This system goes a step further by answering:

> "What should the business do next?"

By combining predictive modeling with AI-driven interpretation, the project simulates a real-world decision intelligence system, not just a modeling exercise.

----

## Tech Stack

- **Python**: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Requests
- **SQL**: PostgreSQL  
- **BI & Storytelling**: Power BI, PowerPoint
- **Version Control**: Git & GitHub  


## 📁 Project Structure

```
customer-retention-optimization/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── transactions.csv
│   │   └── interactions.csv
│   │
│   └── processed/
│       ├── customer_features.csv
│       ├── dashboard_dataset.csv
│       ├── modeling_dataset.csv
│       └── scoring_output.csv
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_optimization.ipynb
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_data_validation.sql
│   ├── 03_data_exploration.sql
│   └── 04_feature_engineering.sql
│
├── models/
│   ├── churn_model.joblib
│   ├── churn_scaler.joblib
│   ├── purchase_drop_cols.joblib
│   ├── purchase_model.joblib
│   └── purchase_scaler.joblib
│
├── src/
│   ├── data_generation.py
│   ├── feature_engineering.py
│   ├── fix_scoring_ids.py
│   ├── modeling.py
│   ├── optimization.py
│   └── ai_integration.py
│
└── reports
    ├── crros_dashboard.pbix
    ├── crros_dashboard_static.pdf
    ├── crros_presentation.pptx
    └── crros_presentation_static.pdf
```


---

## How to Run?

1. Clone the repository  
2. Generate data using Python scripts  
3. Load data into PostgreSQL  
4. Run SQL scripts for feature engineering  
5. Train models and generate predictions  
6. Run optimization script  
7. Visualize results in Power BI  


## Conclusion

This project demonstrates how data science can move beyond prediction to:
- Support decision-making  
- Optimize resource allocation  
- Drive measurable business impact  


## 🤝 Connect

If you found this interesting or have feedback, feel free to follow and connect!

My Portfolio & Profiles: 
- **[Portfolio](https://nibeditans.github.io/)**
- **[LinkedIn](https://www.linkedin.com/in/ns-nibedita-sahu/)**
- **[Medium](https://nsdsda.medium.com/)**
- **[Kaggle](https://www.kaggle.com/nibeditasahu)**
- **[Hackerrank](https://www.hackerrank.com/profile/nibeditans)**

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
