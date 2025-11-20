#include <DHT.h>

#define DHTPIN 4         // DHT11 data pin -> GPIO4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MQ135_PIN 34     // MQ135 AO -> GPIO34 (analog input)

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  int mq_raw = analogRead(MQ135_PIN);  // ESP32: 0–4095 range

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  // Basic scaling (placeholder)
  float co    = mq_raw * 0.01;
  float no2   = mq_raw * 0.008;
  float so2   = mq_raw * 0.006;
  float ozone = mq_raw * 0.012;

  // CSV print: CO,NO2,SO2,Ozone,Temp,Hum
  Serial.print(co, 3);   Serial.print(",");
  Serial.print(no2, 3);  Serial.print(",");
  Serial.print(so2, 3);  Serial.print(",");
  Serial.print(ozone, 3);Serial.print(",");
  Serial.print(temp);    Serial.print(",");
  Serial.println(hum);

  delay(3000);
}
