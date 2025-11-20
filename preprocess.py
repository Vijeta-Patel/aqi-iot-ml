import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
from pathlib import Path

# -------------------------
# File paths
# -------------------------
RAW_PATH = Path("data/raw/final_dataset.csv")
PROCESSED_PATH = Path("data/processed/clean_normalized_dataset.csv")
SCALER_PATH = Path("data/processed/scaler.pkl")


# Columns your sensors can match (MQ135 + DHT11)
FEATURE_COLS = ["NO2", "SO2", "CO", "Ozone", "Month", "Days"]


# -------------------------
# Load dataset
# -------------------------
def load_data():
    df = pd.read_csv(RAW_PATH)
    return df


# -------------------------
# Clean dataset
# -------------------------
def clean_data(df):
    # Drop rows where important values are missing
    df = df.dropna(subset=["NO2", "SO2", "CO", "Ozone", "AQI"])
    return df


# -------------------------
# Convert AQI → Category Name
# -------------------------
def create_aqi_class(df):
    def categorize(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        elif aqi <= 400:
            return "Dangerous"
        else:
            return "Hazardous"

    df["AQI_Class"] = df["AQI"].apply(categorize)
    return df


# -------------------------
# Normalize features for ML model
# -------------------------
def normalize_data(df):
    scaler = MinMaxScaler()
    df[FEATURE_COLS] = scaler.fit_transform(df[FEATURE_COLS])

    # Save scaler to use on live sensor readings
    joblib.dump(scaler, SCALER_PATH)

    return df


# -------------------------
# MAIN EXECUTION
# -------------------------
def main():
    df = load_data()
    df = clean_data(df)
    df = create_aqi_class(df)
    df = normalize_data(df)

    # Save processed dataset
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("\n✔ Preprocessing complete.")
    print("➡ Clean file saved at:", PROCESSED_PATH)
    print("➡ Scaler saved at:", SCALER_PATH)


if __name__ == "__main__":
    main()
