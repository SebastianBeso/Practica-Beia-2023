import time
import RPi.GPIO as GPIO
import json
import paho.mqtt.publish as publish



GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)

MQTT_HOST = 'mqtt.beia-telemetrie.ro'
MQTT_TOPIC = 'training/device/BesoiuSebastian'

 
while True:
    
    foc = GPIO.input(5)
    time.sleep(1)
    if foc==0:
        print ("Este foc")
    elif foc==1:
        print ("Nu este foc")
    time.sleep(5)

    payload_dict={
                  "Foc": foc
                 }
    message = " Foc " + str(foc)
    try:
        publish.single(MQTT_TOPIC, qos=1, hostname=MQTT_HOST, payload=json.dumps(payload_dict))
    except:
        pass

time.sleep(5)
GPIO.cleanup()
