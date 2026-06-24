from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.app.predict import predict_machine

app = FastAPI(
    title="MSPR MECHA 2 - API Maintenance Prédictive",
    description="API FastAPI permettant de prédire si une machine risque de devenir critique lors d'une prochaine observation à partir du modèle LSTM.",
    version="1.0.0"
)


class MachineInput(BaseModel):
    Machine_ID: int = Field(..., example=1)
    Operation_Mode: str = Field(..., example="Active")
    Temperature_C: float = Field(..., example=72.5)
    Vibration_Hz: float = Field(..., example=4.2)
    Power_Consumption_kW: float = Field(..., example=7.8)
    Network_Latency_ms: float = Field(..., example=25.3)

    Packet_Loss_percent: float = Field(
        ..., alias="Packet_Loss_%", example=1.2
    )

    Quality_Control_Defect_Rate_percent: float = Field(
        ..., alias="Quality_Control_Defect_Rate_%", example=5.6
    )

    Production_Speed_units_per_hr: float = Field(..., example=320.0)
    Predictive_Maintenance_Score: float = Field(..., example=0.35)

    Error_Rate_percent: float = Field(
        ..., alias="Error_Rate_%", example=6.5
    )

    Efficiency_Status: str = Field(..., example="Medium")

    hour: int = Field(..., example=14)
    day: int = Field(..., example=24)
    month: int = Field(..., example=6)
    dayofweek: int = Field(..., example=2)
    time_since_start_min: float = Field(..., example=25000.0)

    class Config:
        populate_by_name = True


@app.get("/")
def root():
    return {
        "message": "API MSPR MECHA 2 opérationnelle",
        "model": "LSTM TensorFlow/Keras",
        "target": "future_critical_machine"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend FastAPI actif"
    }


@app.post("/predict")
def predict(input_data: MachineInput):
    data = input_data.model_dump(by_alias=True)
    result = predict_machine(data)

    return {
        "input": data,
        "result": result
    }