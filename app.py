import streamlit as st
import random

# Streamlit page configuration
st.set_page_config(page_title="GenAI Chatbot", layout="wide")


# Mocked function to simulate GenAI API response
def mock_genai_response(prompt):
    return f"Mock response to: '{prompt}'"


# Function to generate mock fairness metrics
def generate_fairness_metrics(prompt, response):
    # Generate some mock metrics (e.g., random values for demonstration)
    return {
        "Demographic Parity": f"{random.uniform(0.8, 1.0):.2f}",
        "Equal Opportunity": f"{random.uniform(0.7, 0.9):.2f}",
        "Predictive Parity": f"{random.uniform(0.6, 0.8):.2f}",
        "Disparate Impact": f"{random.uniform(0.5, 1.0):.2f}",
        "Fairness Through Unawareness": f"{random.uniform(0.4, 0.7):.2f}",
    }


# Streamlit app
def main():
    st.title("GenAI Chatbot")

    # Create two columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Fairness Metrics")

        metrics_info = {
            "Demographic Parity": "Ensures that the decision-making process is fair across different demographic groups.",
            "Equal Opportunity": "Ensures that individuals in different groups have equal chances of receiving a positive outcome.",
            "Predictive Parity": "Ensures that the accuracy of predictions is similar across different groups.",
            "Disparate Impact": "Measures the extent to which a decision disproportionately affects different groups.",
            "Fairness Through Unawareness": "Ensures that sensitive attributes are not used in the decision-making process.",
        }

        for metric, description in metrics_info.items():
            with st.expander(metric):
                st.write("Range: 0 = poor, 1 = best")
                st.write(description)

    with col2:
        # Apply the main panel's color
        st.markdown('<div class="main">', unsafe_allow_html=True)

        # Session state for maintaining chat history
        if "history" not in st.session_state:
            st.session_state.history = []

        # Input text
        user_input = st.text_input("You:", "")

        if st.button("Send") or user_input:
            # Append user input to history
            st.session_state.history.append({"role": "user", "content": user_input})

            # Get response from the mocked GenAI
            genai_response = mock_genai_response(user_input)

            # Append mocked GenAI response to history
            st.session_state.history.append(
                {"role": "genai", "content": genai_response}
            )

        # Display chat history with combined dropdown
        index = 0
        while index < len(st.session_state.history):
            user_message = None
            genai_message = None

            # Collect messages for the current dropdown
            if st.session_state.history[index]["role"] == "user":
                user_message = st.session_state.history[index]["content"]
                index += 1
                if (
                    index < len(st.session_state.history)
                    and st.session_state.history[index]["role"] == "genai"
                ):
                    genai_message = st.session_state.history[index]["content"]
                    index += 1

            if user_message or genai_message:
                # Generate and display mock fairness metrics
                metrics = generate_fairness_metrics(user_message, genai_message)
                expander_label = f"You: {user_message} | GenAI: {genai_message}"

                # Determine if any metric is within 0.2 of 1
                has_high_metric = any(float(value) >= 0.8 for value in metrics.values())

                # Red icon if any metric is high
                red_icon = "🔴" if has_high_metric else ""

                # Apply CSS styling for larger font size
                header_style = "font-size: 24px; font-weight: bold;"  # Adjust font size and weight here

                with st.expander(expander_label + " " + red_icon, expanded=False):
                    for metric, value in metrics.items():
                        color_style = "color:red;" if float(value) >= 0.8 else ""
                        st.markdown(
                            f"<div style='{color_style}'><b>{metric}:</b> {value}</div>",
                            unsafe_allow_html=True,
                        )

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
