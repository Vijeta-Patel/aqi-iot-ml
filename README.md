# 🌫️ Real-Time Air Quality Monitoring System (AQI-IoT-ML)

This project is an **IoT + Machine Learning powered air quality monitoring system** built using:

* **ESP32**
* **MQ135 Gas Sensor**
* **DHT11 Temperature & Humidity Sensor**
* **Python ML pipeline**
* **Real-time data logging & AQI category prediction**

It uses a combination of **historical air quality datasets** + **live sensor data** to build a model that predicts **AQI categories**, such as:

* Good
* Moderate
* Unhealthy
* Very Unhealthy
* Dangerous
* Hazardous

Live readings from sensors are processed through the **trained model** and the output is displayed + logged.

---

# 📁 Project Structure

```
aqi-iot-ml/
│
├── data/
│   ├── raw/
│   │   └── final_dataset.csv                  # Original dataset
│   └── processed/
│       ├── clean_normalized_dataset.csv       # After preprocessing
│       ├── scaler.pkl                         # MinMaxScaler for input normalization
│       ├── aqi_model.pkl                      # Trained ML model
│       └── label_encoder.pkl                  # Converts labels ↔ numbers
│
├── data/live/
│   └── my_live_dataset.csv                    # Your own real sensor data (auto-generated)
│
├── ml/
│   └── train_model.py                         # Trains the ML model
│
├── arduino/
│   └── esp32_mq135_dht/
│       └── esp32_mq135_dht.ino                # ESP32 sensor code
│
├── preprocess.py                               # Cleans + normalizes dataset
├── sensor_predict.py                           # Reads ESP32 serial → predicts AQI → logs data
├── test_model.py                               # Test one sample manually
├── requirements.txt                            # Python dependencies
└── README.md  
```

---

# 🚀 Features

### ✔️ End-to-End ML Pipeline

* Preprocessing
* Normalization
* Label encoding
* RandomForest classification
* Saved model + scaler for real-time inference

### ✔️ Real-Time Sensor Integration

ESP32 streams sensor values in CSV format:

```
CO,NO2,SO2,Ozone,Temp,Hum
```

Python listener:

* Normalizes input
* Predicts AQI category
* Prints live warnings
* Saves readings to `my_live_dataset.csv`

### ✔️ Build Your Own Dataset

Every real sensor reading is appended to:

```
data/live/my_live_dataset.csv
```

Use this for retraining later.

### ✔️ Modular, Clean Code

Arduino code, ML code, preprocessing, and live prediction are separated.

---

# 🧠 How the System Works

## 1️⃣ Preprocessing

Run:

```
python preprocess.py
```

This:

* Loads `final_dataset.csv`
* Cleans & normalizes data
* Categorizes AQI
* Saves processed dataset + scaler

---

## 2️⃣ Model Training

Run:

```
python ml/train_model.py
```

This:

* Loads processed dataset
* Trains RandomForest
* Saves model + label encoder

---

## 3️⃣ ESP32 Sensor Reading

Upload the code in:

```
arduino/esp32_mq135_dht/esp32_mq135_dht.ino
```

Reads:

* MQ135 analog gas values
* DHT11 humidity & temperature
  Then sends CSV lines through USB serial.

---

## 4️⃣ Real-Time Prediction

Run:

```
python sensor_predict.py
```

This script:

* Opens ESP32 serial port
* Reads CSV sensor data
* Normalizes using `scaler.pkl`
* Predicts using `aqi_model.pkl`
* Saves readings + predictions to:

  * `data/live/my_live_dataset.csv`
  * `data/processed/live_readings.csv`
* Prints warnings when category is dangerous

Example output:

```
2025-02-03 RAW=3.432,1.981,1.123,4.550,28.2,54.1 => AQI=Moderate
```

---

# 🛠️ Hardware Setup

### 🔌 Sensors

* ESP32 DevKit V1
* MQ135 (Air Quality Sensor)
* DHT11 (Temperature & Humidity)

### 🪛 Wiring

#### MQ135 → ESP32

| MQ135 Pin | ESP32 Pin |
| --------- | --------- |
| AO        | GPIO34    |
| VCC       | 5V        |
| GND       | GND       |

#### DHT11 → ESP32

| DHT Pin | ESP32 Pin |
| ------- | --------- |
| VCC     | 3.3V      |
| DATA    | GPIO4     |
| GND     | GND       |

---

# 🧪 Testing Without Hardware

Run:

```
python test_model.py
```

Outputs something like:

```
Predicted AQI Category: Unhealthy
```

---

# 🔧 Requirements

```
pandas
scikit-learn
joblib
pyserial
```

Install:

```
pip install -r requirements.txt
```

---

# 🎯 Future Improvements

* Better MQ135 calibration
* ThingSpeak/MQTT integration
* Mobile app dashboard
* Live charts


**Vijeta Patel**
GitHub: [https://github.com/Vijeta-Patel](https://github.com/Vijeta-Patel)
