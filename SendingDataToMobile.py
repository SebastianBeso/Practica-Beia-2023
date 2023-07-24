import requests
import RPi.GPIO as GPIO
import json
import paho.mqtt.publish as publish
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

MQTT_HOST = 'mqtt.beia-telemetrie.ro'
MQTT_TOPIC = 'training/device/BesoiuSebastian'

sensor = Adafruit_DHT.DHT22
pin = 5

telegram_bot_token = "5822012321:AAF4GHtXNRkc84iXI3nM-8RXJaulkrLdks4"  # Înlocuiește cu token-ul API al bot-ului tău
telegram_chat_id = "-913760745"  # Înlocuiește cu ID-ul chat-ului în care vrei să primești datele

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    time.sleep(1)
    
    if humidity is not None and temperature is not None:
        print('Temperatura={0:0.1f}°C Umiditate={1:0.1f}%'.format(temperature, humidity))
        payload_dict = {
            "Temperatura": temperature,
            "Umiditate": humidity
        }
        
        try:
            publish.single(MQTT_TOPIC, qos=1, hostname=MQTT_HOST, payload=json.dumps(payload_dict))
            
            # Trimite datele către ChatBot
            message = 'Temperatura={0:0.1f}°C Umiditate={1:0.1f}%'.format(temperature, humidity)
            url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
            data = {"chat_id": telegram_chat_id, "text": message}
            requests.post(url, json=data)
            
        except:
            pass
    else:
        print('Nu se poate citi data de la senzorul DHT22. Verifică conexiunile!')
    
    time.sleep(5)

GPIO.cleanup()

