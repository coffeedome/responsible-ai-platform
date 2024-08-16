import os
import streamlit as st

from utils.genai import generate_fairness_metrics, mock_genai_response
from utils.sagemaker_clarify import get_clarify_metrics

s3_bucket_name = os.getenv("S3_BUCKET_NAME", "respai-clarify-bucket")
sagemaker_role_arn = os.getenv(
    "SAGEMAKER_ROLE_ARN", "arn:aws:iam::914295800626:role/sagemaker-clarify-role"
)

# Streamlit page configuration
st.set_page_config(page_title="RespAI", layout="wide")


# Streamlit app
def main():
    st.title("Responsible AI Platform")

    # Initialize session state variables
    if "history" not in st.session_state:
        st.session_state.history = []
    if "use_clarify" not in st.session_state:
        st.session_state.use_clarify = False
    if "show_modal" not in st.session_state:
        st.session_state.show_modal = False
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""

    # Create two columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Fairness Metrics")

        # Toggle for enabling/disabling SageMaker Clarify
        use_sagemaker_clarify = st.checkbox("Use SageMaker Clarify", value=False)

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
        st.markdown('<div class="main">', unsafe_allow_html=True)

        # Update session state with the toggle value
        st.session_state.use_clarify = use_sagemaker_clarify

        # Check if we need to show the error modal
        if st.session_state.show_modal:
            st.error(f"An error occurred: {st.session_state.error_message}")
            if st.button("OK"):
                st.session_state.show_modal = False  # Hide the modal immediately
                st.session_state.error_message = ""  # Clear the error message
                st.session_state.use_clarify = (
                    False  # Go back to original use clarify state
                )
                st.rerun()  # Rerun the script immediately to avoid the double-click issue

        else:
            # Input text
            user_input = st.text_input("You:", "")

            if st.button("Send") or user_input:
                st.session_state.history.append({"role": "user", "content": user_input})

                genai_response = mock_genai_response(user_input)
                st.session_state.history.append(
                    {"role": "genai", "content": genai_response}
                )

            index = 0
            while index < len(st.session_state.history):
                user_message = None
                genai_message = None

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
                    try:
                        if st.session_state.use_clarify:
                            metrics = get_clarify_metrics(
                                user_message,
                                genai_message,
                                s3_bucket_name,
                                sagemaker_role_arn,
                            )
                            if metrics is None:
                                continue  # Skip displaying metrics if an error occurred
                        else:
                            metrics = generate_fairness_metrics(
                                user_message, genai_message
                            )

                        expander_label = f"You: {user_message} | GenAI: {genai_message}"

                        has_high_metric = any(
                            float(value) >= 0.8 for value in metrics.values()
                        )
                        red_icon = "🔴" if has_high_metric else ""

                        header_style = "font-size: 24px; font-weight: bold;"

                        with st.expander(
                            expander_label + " " + red_icon, expanded=False
                        ):
                            for metric, value in metrics.items():
                                color_style = (
                                    "color:red;" if float(value) >= 0.8 else ""
                                )
                                st.markdown(
                                    f"<div style='{color_style}'><b>{metric}:</b> {value}</div>",
                                    unsafe_allow_html=True,
                                )
                    except Exception as e:
                        # If an error occurs, update the session state to show the error modal
                        st.session_state.error_message = str(e)
                        st.session_state.show_modal = True
                        st.rerun()  # Rerun the script to show the modal

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
