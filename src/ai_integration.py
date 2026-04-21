def generate_ai_insight(summary: dict) -> tuple:
    import requests
    
    api_key = "YOUR_API_KEY" # Replace with your actual API key here, I've just given a placeholder... Of course!😐

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    models = [
        "google/gemma-4-26b-a4b-it:free",
        "openai/gpt-oss-120b:free",
        "inclusionai/ling-2.6-flash:free",
        "openrouter/elephant-alpha"
    ]

    prompt = f"""
    You are a business analyst.

    Analyze the following customer data insights and provide:

    1. Key observations
    2. Business interpretation
    3. Recommended actions

    Data:
    {summary}

    Keep it concise and practical.
    """

    for model in models:
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        try:
            res_json = response.json()
        except:
            print("Invalid JSON response:", response.text)
            continue

        if "choices" in res_json:
            return model, res_json["choices"][0]["message"]["content"]
        else:
            print(f"Model {model} failed:", res_json)

    return None, "All models failed. Try again later."

# These numbers are the actual insights I got from my project, not randomly assigned.
summary_dict = {
    "customer_segments": {
        "high_value_churn_rate": 0.183168,
        "medium_value_churn_rate": 0.200099,
        "low_value_churn_rate": 0.211497
    },

    "targeting_summary": {
        "customers_targeted": 1000,
        "avg_churn_probability_targeted": 0.0545,
        "avg_purchase_probability_targeted": 0.9393
    },

    "campaign_performance": {
        "incremental_revenue": 1666141.71,
        "campaign_cost": 50000,
        "net_profit": 1616141.71,
        "profit_per_customer": 1516.14
    }
}

# ---- usage ----
model_used, ai_output = generate_ai_insight(summary_dict)

if model_used is None:
    ai_output = """
AI Insight (Fallback Mode)

Key Observations:
- Low-value customers have the highest churn rate (~21%)
- High-value customers are relatively more stable (~18%)
- Targeted customers show very high purchase probability (~94%)

Business Interpretation:
- Strategy is focused on high conversion likelihood rather than churn prevention
- This indicates a revenue maximization approach

Recommended Actions:
- Continue targeting high purchase probability users
- Design separate retention campaigns for high churn segments
- Monitor long-term churn impact
"""

print(f"Model used: {model_used if model_used else 'Fallback'}")
print(ai_output)
