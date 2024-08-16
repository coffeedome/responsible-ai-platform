# Introduction

This is a demo app for GenAI experiments that leverage tools for using GenAI responsively and effectively.

# Problem statement

One of the problems with using GenAI is a lot of times we:

1. Don't fully understand how it's making the decisions it makes (This is also called Explainable AI)
2. Don't fully understand the cost until it is too late. Users often don't get to chose up front for the "cheapest" model. They are locked into a single or a few options.

This platform does the following:

1. It uses the most robust libraries and tools by allowing users to quickly experiment with different models and see it's Responsible AI metrics. These tools include:

   - SageMaker Clarify
   - BedRock Guardrails and System Prompts
   - AI Fairness 360 (AIF360)

2. It provides metrics and model cards with metrics such as:
   - Historical fairness
   - Warnings about outputs
   - Allows input of policies so that models follow those policies when generating content

# Troubleshooting:

An error occurred: An error occurred (ValidationException) when calling the CreateProcessingJob operation: Invalid image URI YOUR_SAGEMAKER_CLARIFY_IMAGE_URI. Please provide a valid Amazon Elastic Container Registry path of the Docker image to run.
-> Sagemaker clarify URIs: https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-processing-job-configure-container.html
