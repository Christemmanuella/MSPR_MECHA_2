import os
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

SCALER_PATH = os.getenv("SCALER_PATH")
ENCODER_OPERATION_PATH = os.getenv("ENCODER_OPERATION_PATH")
ENCODER_EFFICIENCY_PATH = os.getenv("ENCODER_EFFICIENCY_PATH")
FEATURE_COLS_PATH = os.getenv("FEATURE_COLS_PATH")

scaler = joblib.load(SCALER_PATH)
encoder_operation = joblib.load(ENCODER_OPERATION_PATH)
encoder_efficiency = joblib.load(ENCODER_EFFICIENCY_PATH)

with open(FEATURE_COLS_PATH, "r", encoding="utf-8") as f:
    FEATURE_COLS = [line.strip() for line in f.readlines()]


def preprocess_input(data: dict):
    df = pd.DataFrame([data])

    df["Operation_Mode"] = encoder_operation.transform(df["Operation_Mode"])
    df["Efficiency_Status"] = encoder_efficiency.transform(df["Efficiency_Status"])

    df = df[FEATURE_COLS]

    X_scaled = scaler.transform(df)

    # Le LSTM attend une forme : (samples, timesteps, features)
    X_sequence = np.repeat(X_scaled.reshape(1, 1, -1), 10, axis=1)

    return X_sequence