import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("./datasets/final_data.csv")

# Define sensitive features: can lead to discrimination if not handled carefully
sensitive_features = df(
    [
        "gender",
        "age_group",
        "zip_code",
        "race",
        "ethnicity",
        "sexual_orientation",
        "disability_status",
        "religion",
        "nationality",
        "marital_or_family_status",
        "socioeconomic_background",
        "educational_backgroun",
        "veteran_status",
        "parental_status",
        "geographic_location",
        "political_affiliation",
        "language_proficiency",
        "work_authorization",
        "criminal_record",
        "health_status",
        "weight_height",
        "appearance",
    ]
)

required_complex_data_features = df(
    [
        "candidate_resume",
        "job_descriptions",
        "years_of_experience",
        "previous_employers",  # this one could be sensitive???
    ]
)

# We use traditional models for regression -> more practical for structured data/predictive modelling.
# We use LLM for NLP processing: resume, job descriptions, posts on linked in - for CONTEXTUAL understanding
# We also use LLM for Image processing: appearance, which could be a sensitive feature we need to watch out for!!!

# Split data into features (input vars) and labels (target variable we want to predict)
# Features: All columns except 'Class' which is our label
X = df.drop(columns=["Class"])
# Labels: the 'Class' column
y = df["Class"]
