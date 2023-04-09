import requests
import json
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO

lights = 'Activity Detected, Opening the lights!'
no_lights = 'No Activity Detected for 10 Minutes, Closing the lights!'
webhook_url = "https://webhook.site/c33575f1-8a72-43e3-90e5-dbf3762b66e2"
data = {
    'time': '',
    'status': '',
    'room_no': 'minihall',
    'usage_time': '0'
}
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14,GPIO.IN)
    GPIO.setup(17,GPIO.OUT)

def loop():
    i = 0
    usage_time = 0
    aim_time = 0
    light_status = 0
    while True:
        if GPIO.input(14) == 0:
            sleep(1)
            aim_time += 1
        if i == 0:
            sleep(1)
            usage_time += 1
        if aim_time == 10:     # laser not broken for 10 minutes, sending data to turn off lights
            GPIO.output(17, GPIO.HIGH)
            data['time'] = str(datetime.now())
            data['status'] = no_lights
            data['usage_time'] = str(usage_time)
            r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            light_status = 0
            i = 1

        if light_status == 0:
            if GPIO.input(14) == 1:     # laser broken, sending data to turn on lights

                GPIO.output(17, GPIO.LOW)
                data['time'] = str(datetime.now())
                data['status'] = lights
                r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                aim_time = 0
                light_status=1
                i=0
if __name__ == '__main__':
    setup()
    loop()
