# Import libraries 
import RPi.GPIO as GPIO
from time import sleep 


GPIO.setmode(GPIO.BCM)
ventilator = 6
GPIO.setup(ventilator, GPIO.OUT)




#ventilator
def ventilator_on():
    GPIO.output(ventilator,GPIO.LOW)
def ventilator_off():
    GPIO.output(ventilator,GPIO.HIGH)

ventilator_off()
