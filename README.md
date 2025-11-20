# aqi-iot-ml
Real-time air quality monitoring system using IoT sensors and machine learning. The project trains an initial AQI model using a public dataset and continuously improves it by feeding live sensor data back into the dataset using ESP32, DHT11 and MQ135.


aqi-iot-ml/
│
├── preprocess.py             
├── ml/train_model.py        
├── test_model.py             
├── sensor_predict.py         
│
├── data/
│   ├── raw/
│   │   └── final_dataset.csv
│   └── processed/
│       ├── clean_normalized_dataset.csv
│       ├── scaler.pkl
│       ├── aqi_model.pkl
│       ├── label_encoder.pkl
│       └── live_readings.csv   
