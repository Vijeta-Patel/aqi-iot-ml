# sensor_predict.py
# Reads CSV lines from ESP8266 over serial, predicts AQI using your trained model,
# saves every reading to your live dataset, and prints warnings if needed.

import serial
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# ------------- CONFIG -------------
SERIAL_PORT = "COM5"   # <-- CHANGE THIS to your ESP's COM port
BAUDRATE = 115200

FEATURE_COLS = ["NO2", "SO2", "CO", "Ozone", "Month", "Days"]

# Where to save your real-time readings
MY_LIVE_DIR = Path("data/live")
MY_LIVE_PATH = MY_LIVE_DIR / "my_live_dataset.csv"

# Also saving here (optional)
PROCESSED_LIVE_PATH = Path("data/processed/live_readings.csv")

# Model files
SCALER_PATH = Path("data/processed/scaler.pkl")
MODEL_PATH = Path("data/processed/aqi_model.pkl")
ENCODER_PATH = Path("data/processed/label_encoder.pkl")

# Categories to warn about
ALERT_CATEGORIES = {"Very Unhealthy", "Dangerous", "Hazardous"}

# ------------- Load model artifacts -------------
print("Loading model + scaler + encoder...")
scaler = joblib.load(SCALER_PATH)
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

# ------------- Serial setup -------------
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=3)
    print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baud.")
except Exception as e:
    print(f"ERROR opening serial port {SERIAL_PORT}: {e}")
    raise SystemExit

# ------------- Helper functions -------------
def parse_csv(line):
    """
    ESP prints: CO,NO2,SO2,Ozone,Temp,Hum
    We only use the first 4 values.
    """
    parts = [p.strip() for p in line.split(",") if p.strip() != ""]
    if len(parts) < 4:
        return None
    try:
        co = float(parts[0])
        no2 = float(parts[1])
        so2 = float(parts[2])
        ozone = float(parts[3])
    except:
        return None

    now = datetime.now()

    return {
        "NO2": no2,
        "SO2": so2,
        "CO": co,
        "Ozone": ozone,
        "Month": now.month,
        "Days": now.day,
    }


def save_to_my_live_dataset(sample, label):
    """Save raw readings + predicted label to your OWN dataset."""
    MY_LIVE_DIR.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp": datetime.now().isoformat(),
        "NO2": sample["NO2"],
        "SO2": sample["SO2"],
        "CO": sample["CO"],
        "Ozone": sample["Ozone"],
        "Month": sample["Month"],
        "Days": sample["Days"],
        "AQI_Predicted": label,
    }

    df = pd.DataFrame([row])
    if not MY_LIVE_PATH.exists():
        df.to_csv(MY_LIVE_PATH, index=False)
    else:
        df.to_csv(MY_LIVE_PATH, index=False, header=False, mode="a")


def save_to_processed(sample, label):
    """Save to old processed live file (optional)."""
    PROCESSED_LIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = {"timestamp": datetime.now().isoformat(), **sample, "Predicted_Label": label}

    df = pd.DataFrame([row])
    if not PROCESSED_LIVE_PATH.exists():
        df.to_csv(PROCESSED_LIVE_PATH, index=False)
    else:
        df.to_csv(PROCESSED_LIVE_PATH, index=False, header=False, mode="a")


# ------------- Main Loop -------------
print("Listening for sensor data...\n")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        sample = parse_csv(line)
        if sample is None:
            print("Skipped bad line:", line)
            continue

        # Build DataFrame in expected format
        df = pd.DataFrame([sample], columns=FEATURE_COLS)

        # Normalize
        X = scaler.transform(df)

        # Predict
        y_num = model.predict(X)[0]
        label = encoder.inverse_transform([y_num])[0]

        timestamp = datetime.now().isoformat()

        # Print live result
        print(f"{timestamp}  RAW={line}  =>  AQI={label}")

        # Save both ways
        save_to_my_live_dataset(sample, label)
        save_to_processed(sample, label)

        # Alerts
        if label in ALERT_CATEGORIES:
            print(f"!!! WARNING: Hazardous air detected: {label} !!!")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped.")
    ser.close()
