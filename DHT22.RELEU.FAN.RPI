import time
import RPi.GPIO as GPIO
import json
import paho.mqtt.publish as publish
import Adafruit_DHT
import actionareventilator

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

MQTT_HOST = 'mqtt.beia-telemetrie.ro'
MQTT_TOPIC = 'training/device/BesoiuSebastian'

sensor = Adafruit_DHT.DHT22
pin = 5


while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    time.sleep(1)
    
    if humidity is not None and temperature is not None:
        print('Temperatura={0:0.1f}°C Umiditate={1:0.1f}%'.format(temperature, humidity))
        payload_dict = {
            "Temperatura": temperature,
            "Umiditate": humidity
        }
        if temperature > 28:
            actionareventilator.ventilator_on()
        else:
            actionareventilator.ventilator_off()
        try:
            publish.single(MQTT_TOPIC, qos=1, hostname=MQTT_HOST, payload=json.dumps(payload_dict))
        except:
            pass
    else:
        print('Nu se poate citi data de la senzorul DHT22. Verifică conexiunile!')
    
    time.sleep(5)

GPIO.cleanup()
