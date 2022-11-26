#프로젝트명 
from flask import Flask, request
import RPi.GPIO as GPIO

locker = [17, 27, 22, 10] #locker Id 는 Index - 1번이다

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
for i in locker :
    GPIO.setup(i, GPIO.OUT, inital=GPIO.HIGH) #다 열려있어야함.


@app.route("/open") #라커 문을 여는 API이다.
def openLocker():
    try:
        params = request.get_json()
        lockerId = params['lockerId']
        GPIO.output(lockerId, GPIO.HIGH) #딱 하고 열림..
        GPIO.output(lockerId, GPIO.LOW)
        return True
    except :
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0")
