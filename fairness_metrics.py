import streamlit as st


def display_fairness_metrics(model_name, response):
    metrics = {
        "Bias Score": 0.5,  # Example metric
        "Fairness Index": 0.8,  # Example metric
    }

    st.subheader("Fairness Metrics")
    st.write(f"Response: {response}")

    st.write("Metrics:")
    for metric, value in metrics.items():
        st.write(f"{metric}: {value}")
