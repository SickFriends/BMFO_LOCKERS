#프로젝트명 
from flask import Flask
from flask import request
from flask import render_template
import webbrowser
# import RPi.GPIO as GPIO

locker = [17, 27, 22, 10] #locker Id 는 Index - 1번이다

app = Flask(__name__)

# GPIO.setmode(GPIO.BCM)
# for i in locker :
#     GPIO.setup(i, GPIO.OUT, inital=GPIO.HIGH) #다 열려있어야함.


@app.post("/openLockerFromCustommer") #라커 문을 여는 API이다.
def open():
    params = request.get_json()
    lockerId = params['lockerId']
    orderId = params['orderId']
    # GPIO.output(lockerId, GPIO.HIGH) #딱 하고 열림..
    # GPIO.output(lockerId, GPIO.LOW)
    webbrowser.open("http://localhost:8000/showToCustommer?orderId=" + orderId)
    return "okay"

@app.post("/openLockerFromSeller") #라커 문을 여는 API이다.
def openForSeller():
    params = request.get_json()
    lockerId = params['lockerId']
    # GPIO.output(lockerId, GPIO.HIGH) #딱 하고 열림..
    # GPIO.output(lockerId, GPIO.LOW)
    return "okay"

@app.get('/showToCustommer')
def showToCustommer() :
    args = request.args
    orderId  = args.get("orderId")
    print(orderId)
    return render_template("showToCustommer.html", orderId = orderId)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
