import board
import adafruit_dht
import time
import paho.mqtt.client as mqtt
import json

dhtDevice = adafruit_dht.DHT22(board.D17)
client = mqtt.Client()
client.connect("localhost", 1883, 60)

print("Mulai publish data DHT22 ke MQTT topic 'sensor/dht22'...")
print("Tekan Ctrl+C untuk berhenti")

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        payload = json.dumps({"temperature": temperature, "humidity": humidity})
        client.publish("sensor/dht22", payload)
        print(f"Published: {payload}")
    except RuntimeError as e:
        print(f"Gagal baca sensor (retry otomatis): {e.args[0]}")
    except KeyboardInterrupt:
        print("Berhenti.")
        dhtDevice.exit()
        break
    time.sleep(5)
