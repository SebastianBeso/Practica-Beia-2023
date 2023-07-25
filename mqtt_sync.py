import os
import json
import time
import paho.mqtt.client as mqtt

# Configurare pentru conexiunea MQTT
mqtt_host = "mqtt.beia-telemetrie.ro"
mqtt_topic = "training/device/BesoiuSebastian"
mqtt_client_id = "candidat_mqtt_sync"

# Folder pentru stocarea datelor
data_folder = "candidatBesoiuSebastian"

def read_local_data():
    filename = os.path.join(data_folder, "data.json")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    return None

def on_connect(client, userdata, flags, rc):
    print("Conectat la serverul MQTT")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Mesaj primit: {msg.payload}")

def main():
    client = mqtt.Client(client_id=mqtt_client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            client.connect(mqtt_host, 1883, 60)
            break
        except ConnectionRefusedError:
            print("Conexiunea la serverul MQTT a eșuat. Reîncercare în 5 secunde...")
            time.sleep(5)

    client.loop_start()

    while True:
        data = read_local_data()
        if data:
            payload = json.dumps(data)
            client.publish(mqtt_topic, payload, qos=1)
            print("Datele au fost trimise către cloud:", data)
        else:
            print("Nu există date locale de trimis către cloud.")

        time.sleep(60)  # Așteaptă 60 de secunde înainte de a verifica din nou

if __name__ == "__main__":
    main()

