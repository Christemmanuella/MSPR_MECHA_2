import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "data" / "processed" / "mecha_feature_engineered.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "mecha_final_dataset.csv"


def create_final_dataset():
    df = pd.read_csv(INPUT_PATH)

    print("Dataset chargé :", df.shape)

    # Suppression des colonnes intermédiaires pour éviter la fuite de données
    leakage_cols = [
        "temperature_alert",
        "vibration_alert",
        "maintenance_risk",
        "quality_alert",
        "global_risk_score"
    ]

    df = df.drop(columns=leakage_cols, errors="ignore")

    df.to_csv(OUTPUT_PATH, index=False)

    print("Dataset final créé :", df.shape)
    print("Fichier sauvegardé :", OUTPUT_PATH)


if __name__ == "__main__":
    create_final_dataset()