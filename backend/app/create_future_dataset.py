import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "data" / "processed" / "mecha_temporal_dataset.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "mecha_future_dataset.csv"


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Dataset chargé :", df.shape)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    df = df.sort_values(["Machine_ID", "Timestamp"]).reset_index(drop=True)

    # Nouvelle cible temporelle :
    # est-ce que la machine sera critique à la prochaine observation ?
    df["future_critical_machine"] = (
        df.groupby("Machine_ID")["critical_machine"].shift(-1)
    )

    # On supprime les dernières lignes de chaque machine car elles n'ont pas de futur connu
    df = df.dropna(subset=["future_critical_machine"])

    df["future_critical_machine"] = df["future_critical_machine"].astype(int)

    # Colonnes à supprimer pour éviter la triche
    leakage_cols = [
        "temperature_alert",
        "vibration_alert",
        "maintenance_risk",
        "quality_alert",
        "global_risk_score",
        "critical_machine"
    ]

    df = df.drop(columns=leakage_cols, errors="ignore")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("Nouveau dataset créé :", df.shape)
    print("Fichier sauvegardé :", OUTPUT_PATH)
    print("Nouvelle cible :", "future_critical_machine")
    print(df["future_critical_machine"].value_counts())


if __name__ == "__main__":
    main()