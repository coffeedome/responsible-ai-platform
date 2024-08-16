import boto3
import json
import time
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sagemaker = boto3.client("sagemaker")
s3 = boto3.client("s3")


def get_clarify_metrics(
    user_message, genai_message, s3_bucket: str, sagemaker_role_arn: str
):
    try:
        logger.info("Starting SageMaker Clarify processing job")

        # Store the chat response in S3
        input_data = {"user_message": user_message, "genai_message": genai_message}
        input_s3_uri = f"s3://{s3_bucket}/input_data.json"
        logger.info(f"Uploading input data to S3: {input_s3_uri}")
        s3.put_object(
            Bucket=s3_bucket, Key="input_data.json", Body=json.dumps(input_data)
        )

        # Trigger SageMaker Clarify processing job
        processing_job_name = f"clarify-job-{int(time.time())}"
        logger.info(f"Creating processing job: {processing_job_name}")

        response = sagemaker.create_processing_job(
            ProcessingJobName=processing_job_name,
            RoleArn=sagemaker_role_arn,
            ProcessingInputs=[
                {
                    "InputName": "input-1",
                    "S3Input": {
                        "S3Uri": input_s3_uri,
                        "LocalPath": "/opt/ml/processing/input",
                        "S3DataType": "S3Prefix",
                        "S3InputMode": "File",
                    },
                }
            ],
            ProcessingOutputConfig={
                "Outputs": [
                    {
                        "OutputName": "clarify-output",
                        "S3Output": {
                            "S3Uri": f"s3://{s3_bucket}/output/",
                            "LocalPath": "/opt/ml/processing/output",
                            "S3UploadMode": "EndOfJob",
                        },
                    }
                ]
            },
            ProcessingResources={
                "ClusterConfig": {
                    "InstanceCount": 1,
                    "InstanceType": "ml.t3.medium",  # Use a smaller instance type
                    "VolumeSizeInGB": 30,
                }
            },
            StoppingCondition={"MaxRuntimeInSeconds": 60},
            AppSpecification={
                "ImageUri": "306415355426.dkr.ecr.us-west-2.amazonaws.com/sagemaker-clarify-processing:1.0",
                "ContainerEntrypoint": [
                    "python3",
                    "/opt/ml/processing/input/clarify_script.py",
                ],
            },
        )

        logger.info("Processing job created successfully. Waiting for completion...")

        # Poll for job completion
        while True:
            job_status = sagemaker.describe_processing_job(
                ProcessingJobName=processing_job_name
            )["ProcessingJobStatus"]
            logger.info(f"Job status: {job_status}")
            if job_status in ["Completed", "Failed"]:
                break
            time.sleep(30)

        if job_status == "Completed":
            # Retrieve metrics from S3
            output_s3_uri = f"s3://{s3_bucket}/output/clarify_output.json"
            logger.info(f"Job completed. Fetching results from S3: {output_s3_uri}")
            response = s3.get_object(Bucket=s3_bucket, Key="output/clarify_output.json")
            metrics = json.loads(response["Body"].read().decode("utf-8"))
            logger.info(f"Metrics retrieved: {metrics}")
            return metrics
        else:
            logger.error("Clarify processing job failed")
            st.session_state.show_modal = True
            st.session_state.error_message = "Clarify processing job failed"
            return None

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        st.session_state.show_modal = True
        st.session_state.error_message = str(e)
        return None
