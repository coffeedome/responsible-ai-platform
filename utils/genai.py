import random


# Mocked function to simulate GenAI API response (replace with actual GenAI API call)
def mock_genai_response(prompt):
    return f"Mock response to: '{prompt}'"


def generate_fairness_metrics(prompt, response):
    # Generate some mock metrics (e.g., random values for demonstration)
    return {
        "Demographic Parity": f"{random.uniform(0.8, 1.0):.2f}",
        "Equal Opportunity": f"{random.uniform(0.7, 0.9):.2f}",
        "Predictive Parity": f"{random.uniform(0.6, 0.8):.2f}",
        "Disparate Impact": f"{random.uniform(0.5, 1.0):.2f}",
        "Fairness Through Unawareness": f"{random.uniform(0.4, 0.7):.2f}",
    }
