import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_PATH = BASE_DIR / "data" / "bronze" / "mecha_dataset_bronze.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(BRONZE_PATH)
    print("Dataset chargé :", df.shape)
    return df


def create_features(df):
    df["temperature_alert"] = (df["Temperature_C"] > 90).astype(int)
    df["vibration_alert"] = (df["Vibration_Hz"] > 6).astype(int)

    df["maintenance_risk"] = (
        df["Predictive_Maintenance_Score"] < 0.3
    ).astype(int)

    df["quality_alert"] = (
        df["Quality_Control_Defect_Rate_%"] > 8
    ).astype(int)

    df["global_risk_score"] = (
        df["temperature_alert"]
        + df["vibration_alert"]
        + df["maintenance_risk"]
        + df["quality_alert"]
    )

    df["critical_machine"] = (
        df["global_risk_score"] >= 2
    ).astype(int)

    return df


def save_dataset(df):
    output_path = PROCESSED_DIR / "mecha_feature_engineered.csv"
    df.to_csv(output_path, index=False)

    print("Dataset enrichi sauvegardé :", output_path)
    print("Nouvelle taille :", df.shape)


if __name__ == "__main__":
    df = load_data()
    df = create_features(df)
    save_dataset(df)