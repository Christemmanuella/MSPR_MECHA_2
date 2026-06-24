CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,

    machine_id INTEGER NOT NULL,
    operation_mode VARCHAR(50),

    temperature_c FLOAT,
    vibration_hz FLOAT,
    power_consumption_kw FLOAT,
    network_latency_ms FLOAT,
    packet_loss_percent FLOAT,
    quality_control_defect_rate_percent FLOAT,
    production_speed_units_per_hr FLOAT,
    predictive_maintenance_score FLOAT,
    error_rate_percent FLOAT,
    efficiency_status VARCHAR(50),

    hour INTEGER,
    day INTEGER,
    month INTEGER,
    dayofweek INTEGER,
    time_since_start_min FLOAT,

    prediction INTEGER NOT NULL,
    probability FLOAT NOT NULL,
    risk_label VARCHAR(100),
    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,

    prediction_id INTEGER REFERENCES predictions(id) ON DELETE CASCADE,
    machine_id INTEGER NOT NULL,
    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);