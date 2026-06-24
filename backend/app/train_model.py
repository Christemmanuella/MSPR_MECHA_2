import pandas as pd
import joblib
from pathlib import Path

from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_PATH = BASE_DIR / "data" / "processed" / "train.csv"
TEST_PATH = BASE_DIR / "data" / "processed" / "test.csv"
MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print("Train chargé :", train_df.shape)
    print("Test chargé :", test_df.shape)

    return train_df, test_df


def prepare_features(train_df, test_df):
    leakage_columns = [
        "critical_machine",
        "temperature_alert",
        "vibration_alert",
        "maintenance_risk",
        "quality_alert",
        "global_risk_score"
    ]

    X_train = train_df.drop(columns=leakage_columns, errors="ignore")
    y_train = train_df["critical_machine"]

    X_test = test_df.drop(columns=leakage_columns, errors="ignore")
    y_test = test_df["critical_machine"]

    X_train = pd.get_dummies(X_train, drop_first=True)
    X_test = pd.get_dummies(X_test, drop_first=True)

    X_train, X_test = X_train.align(
        X_test,
        join="left",
        axis=1,
        fill_value=0
    )

    print("Nombre de features utilisées :", X_train.shape[1])

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n===== RÉSULTATS XGBOOST =====")
    print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred):.4f}")
    print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
    print(f"F1-score  : {f1_score(y_test, y_pred):.4f}")
    print(f"ROC AUC   : {roc_auc_score(y_test, y_proba):.4f}")

    print("\n===== RAPPORT DE CLASSIFICATION =====")
    print(classification_report(y_test, y_pred))

    print("\n===== MATRICE DE CONFUSION =====")
    print(confusion_matrix(y_test, y_pred))


def save_model(model):
    model_path = MODELS_DIR / "xgboost_model.pkl"
    joblib.dump(model, model_path)

    print("\nModèle sauvegardé :", model_path)


if __name__ == "__main__":
    train_df, test_df = load_data()
    X_train, X_test, y_train, y_test = prepare_features(train_df, test_df)

    model = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    save_model(model)