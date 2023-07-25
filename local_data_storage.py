import os
import json
import RPi.GPIO as GPIO
import Adafruit_DHT

# Configurare pin DHT22 și senzor
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)
sensor = Adafruit_DHT.DHT22
pin = 5

# Folder pentru stocarea datelor
data_folder = "candidatBesoiuSebastian"

def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

def store_data_locally(data):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    filename = os.path.join(data_folder, "data.json")
    with open(filename, "w") as file:
        json.dump(data, file)

def main():
    humidity, temperature = read_sensor_data()
    if humidity is not None and temperature is not None:
        data = {
            "Temperatura": temperature,
            "Umiditate": humidity
        }
        store_data_locally(data)
        print("Datele au fost stocate local:", data)
    else:
        print("Nu s-au putut citi datele de la senzorul DHT22.")

if __name__ == "__main__":
    main()

