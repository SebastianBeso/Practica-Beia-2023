import RPi.GPIO as GPIO
import json
import paho.mqtt.publish as publish
import Adafruit_DHT
import time
import requests
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import speech_recognition as sr

# Restul codului rămâne neschimbat
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

MQTT_HOST = 'mqtt.beia-telemetrie.ro'
MQTT_TOPIC = 'training/device/BesoiuSebastian'

sensor = Adafruit_DHT.DHT22
pin = 5

telegram_bot_token = "5822012321:AAF4GHtXNRkc84iXI3nM-8RXJaulkrLdks"  # Înlocuiește cu token-ul API al bot-ului tău
telegram_chat_id = "-913760745"    # Înlocuiește cu ID-ul chat-ului în care vrei să primești datele

def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

def send_data_to_mqtt(humidity, temperature):
    payload_dict = {
        "Temperatura": temperature,
        "Umiditate": humidity
    }
    try:
        publish.single(MQTT_TOPIC, qos=1, hostname=MQTT_HOST, payload=json.dumps(payload_dict))
    except:
        pass

def send_data_to_telegram(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message}
    requests.post(url, json=data)

def handle_voice_message(update, context):
    file_info = update.message.voice.get_file()
    file_url = file_info.file_path

    # Transcrie mesajul vocal în text
    recognizer = sr.Recognizer()
    response = ""

    try:
        with sr.AudioFile(file_url) as source:
            audio_text = recognizer.recognize_google(source)
            audio_text_lower = audio_text.lower()

            # Verifică cererile referitoare la temperatură și umiditate
            if "temperatura" in audio_text_lower:
                humidity, temperature = read_sensor_data()
                if temperature is not None:
                    response = f"Ultima valoare a temperaturii: {temperature:.1f}°C"
                else:
                    response = "Nu s-au citit încă date despre temperatură."
            elif "umiditate" in audio_text_lower:
                humidity, temperature = read_sensor_data()
                if humidity is not None:
                    response = f"Ultima valoare a umidității: {humidity:.1f}%"
                else:
                    response = "Nu s-au citit încă date despre umiditate."
            else:
                response = "Comandă nevalidă. Poți întreba 'temperatura' sau 'umiditate'."

    except sr.UnknownValueError:
        response = "Nu am putut transcrie mesajul tău vocal. Te rog încearcă din nou."

    send_data_to_telegram(response)

    # Trimite datele către MQTT
    humidity, temperature = read_sensor_data()
    send_data_to_mqtt(humidity, temperature)

# Creează un obiect Updater și specifică un update_queue gol
updater = Updater(telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

# Adaugă handler pentru gestionarea mesajelor vocale primite
dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice_message))

# Pornirea bot-ului
updater.start_polling()

# Menține bot-ul activ
updater.idle()

GPIO.cleanup()
