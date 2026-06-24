import os
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from sqlalchemy import text

from backend.app.preprocess import preprocess_input
from backend.app.database import engine

load_dotenv(dotenv_path="backend/.env")

MODEL_PATH = os.getenv("MODEL_PATH")

if not MODEL_PATH:
    raise ValueError("MODEL_PATH est introuvable dans backend/.env")

model = load_model(MODEL_PATH)


def save_prediction_to_db(data: dict, result: dict):
    insert_prediction_query = text("""
        INSERT INTO predictions (
            machine_id,
            operation_mode,
            temperature_c,
            vibration_hz,
            power_consumption_kw,
            network_latency_ms,
            packet_loss_percent,
            quality_control_defect_rate_percent,
            production_speed_units_per_hr,
            predictive_maintenance_score,
            error_rate_percent,
            efficiency_status,
            hour,
            day,
            month,
            dayofweek,
            time_since_start_min,
            prediction,
            probability,
            risk_label,
            message
        )
        VALUES (
            :machine_id,
            :operation_mode,
            :temperature_c,
            :vibration_hz,
            :power_consumption_kw,
            :network_latency_ms,
            :packet_loss_percent,
            :quality_control_defect_rate_percent,
            :production_speed_units_per_hr,
            :predictive_maintenance_score,
            :error_rate_percent,
            :efficiency_status,
            :hour,
            :day,
            :month,
            :dayofweek,
            :time_since_start_min,
            :prediction,
            :probability,
            :risk_label,
            :message
        )
        RETURNING id;
    """)

    prediction_data = {
        "machine_id": data["Machine_ID"],
        "operation_mode": data["Operation_Mode"],
        "temperature_c": data["Temperature_C"],
        "vibration_hz": data["Vibration_Hz"],
        "power_consumption_kw": data["Power_Consumption_kW"],
        "network_latency_ms": data["Network_Latency_ms"],
        "packet_loss_percent": data["Packet_Loss_%"],
        "quality_control_defect_rate_percent": data["Quality_Control_Defect_Rate_%"],
        "production_speed_units_per_hr": data["Production_Speed_units_per_hr"],
        "predictive_maintenance_score": data["Predictive_Maintenance_Score"],
        "error_rate_percent": data["Error_Rate_%"],
        "efficiency_status": data["Efficiency_Status"],
        "hour": data["hour"],
        "day": data["day"],
        "month": data["month"],
        "dayofweek": data["dayofweek"],
        "time_since_start_min": data["time_since_start_min"],
        "prediction": result["prediction"],
        "probability": result["probability"],
        "risk_label": result["risk_label"],
        "message": result["message"]
    }

    with engine.begin() as connection:
        prediction_id = connection.execute(
            insert_prediction_query,
            prediction_data
        ).scalar_one()

        if result["prediction"] == 1:
            insert_alert_query = text("""
                INSERT INTO alerts (
                    prediction_id,
                    machine_id,
                    message
                )
                VALUES (
                    :prediction_id,
                    :machine_id,
                    :message
                );
            """)

            connection.execute(
                insert_alert_query,
                {
                    "prediction_id": prediction_id,
                    "machine_id": data["Machine_ID"],
                    "message": result["message"]
                }
            )

    return prediction_id


def predict_machine(data: dict):
    X_sequence = preprocess_input(data)

    probability = float(model.predict(X_sequence, verbose=0)[0][0])
    prediction = int(probability >= 0.5)

    if prediction == 1:
        risk_label = "Risque critique futur"
        message = "La machine présente un risque de devenir critique lors d'une prochaine observation. Une intervention préventive est recommandée."
    else:
        risk_label = "Risque faible"
        message = "Aucun risque critique futur majeur n'est détecté pour cette machine."

    result = {
        "prediction": prediction,
        "probability": round(probability, 4),
        "risk_label": risk_label,
        "message": message
    }

    prediction_id = save_prediction_to_db(data, result)

    result["prediction_id"] = prediction_id

    return result