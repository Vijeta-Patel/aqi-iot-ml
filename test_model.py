import joblib
import pandas as pd
from datetime import datetime

# paths
MODEL_PATH = "data/processed/aqi_model.pkl"
SCALER_PATH = "data/processed/scaler.pkl"
ENCODER_PATH = "data/processed/label_encoder.pkl"

# features used in training
FEATURE_COLS = ["NO2", "SO2", "CO", "Ozone", "Month", "Days"]

# load model + scaler + encoder
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoder = joblib.load(ENCODER_PATH)

# test sample (you can change these later)
sample = {
    "NO2": 40,
    "SO2": 10,
    "CO": 2.5,
    "Ozone": 30,
    "Month": datetime.now().month,
    "Days": datetime.now().day
}

df = pd.DataFrame([sample], columns=FEATURE_COLS)

# scale input
X = scaler.transform(df)

# predict numeric class
y_pred = model.predict(X)[0]

# convert numeric class → text label
label = encoder.inverse_transform([y_pred])[0]

print("\nINPUT:", sample)
print("AQI CATEGORY Predicted:", label)
