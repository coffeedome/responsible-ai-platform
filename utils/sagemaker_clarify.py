import boto3
import json
import time
import streamlit as st

sagemaker = boto3.client("sagemaker")
s3 = boto3.client("s3")


def get_clarify_metrics(
    user_message, genai_message, s3_bucket: str, sagemaker_role_arn: str
):
    # Store the chat response in S3
    input_data = {"user_message": user_message, "genai_message": genai_message}
    input_s3_uri = f"s3://{s3_bucket}/input_data.json"
    s3.put_object(Bucket=s3_bucket, Key="input_data.json", Body=json.dumps(input_data))

    # Trigger SageMaker Clarify processing job
    processing_job_name = f"clarify-job-{int(time.time())}"
    try:
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
            ProcessingJobConfig={
                "ProcessingResources": {
                    "ClusterConfig": {
                        "InstanceCount": 1,
                        "InstanceType": "ml.m5.xlarge",
                        "VolumeSizeInGB": 30,
                    }
                },
                "StoppingCondition": {"MaxRuntimeInSeconds": 60},
            },
            AppSpecification={
                "ImageUri": "YOUR_SAGEMAKER_CLARIFY_IMAGE_URI",
                "ContainerEntrypoint": [
                    "python3",
                    "/opt/ml/processing/input/clarify_script.py",
                ],
            },
        )
        # Poll for job completion
        while True:
            job_status = sagemaker.describe_processing_job(
                ProcessingJobName=processing_job_name
            )["ProcessingJobStatus"]
            if job_status in ["Completed", "Failed"]:
                break
            time.sleep(30)

        if job_status == "Completed":
            # Retrieve metrics from S3
            output_s3_uri = f"s3://{s3_bucket}/output/clarify_output.json"
            response = s3.get_object(Bucket=s3_bucket, Key="output/clarify_output.json")
            metrics = json.loads(response["Body"].read().decode("utf-8"))
            print("DEBUG_START")
            print(metrics)
            print("DEBUG_END")
            return metrics
        else:
            st.session_state.show_modal = True
            st.session_state.error_message = "Clarify processing job failed"
            return None

    except Exception as e:
        st.session_state.show_modal = True
        st.session_state.error_message = str(e)
        return None
