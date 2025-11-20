# ml/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path

# --- paths ---
DATA_PATH = Path("data/processed/clean_normalized_dataset.csv")
MODEL_PATH = Path("data/processed/aqi_model.pkl")
ENCODER_PATH = Path("data/processed/label_encoder.pkl")

# --- features used in preprocessing ---
FEATURE_COLS = ["NO2", "SO2", "CO", "Ozone", "Month", "Days"]

def main():
    print("Loading processed dataset:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)

    # quick sanity check
    missing = [c for c in FEATURE_COLS + ["AQI_Class"] if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing columns in processed CSV: {missing}")

    X = df[FEATURE_COLS]
    y = df["AQI_Class"]  # string labels like "Good","Moderate",...

    # encode labels to numeric
    encoder = LabelEncoder()
    y_enc = encoder.fit_transform(y)

    # train model
    print("Training RandomForest (may take a little)...")
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y_enc)

    # save model and encoder
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print("Training complete.")
    print("Model saved to:", MODEL_PATH)
    print("Label encoder saved to:", ENCODER_PATH)

if __name__ == "__main__":
    main()
