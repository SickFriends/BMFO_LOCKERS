import sys
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# import RPi.GPIO as GPIO
from time import sleep

led = [17, 27, 22, 10]
url = "http://10.150.149.50:8000/api/locker/open"

def set_GPIO():
    return
#    GPIO.setmode(GPIO.BCM)
#    for item in led:
#       GPIO.setup(item, GPIO.OUT)

def server(lckNum, password):
   datas = {
      'id' : lckNum,
      'pass' : password
   }
   headers = {'Content-type': 'application/json', 'Accept': 'text/json'}
   res = req.post(url, json=datas, headers=headers)
   
   print(res.json())
   a = res.json()
   if a['SUCCESS']==True:
      print("opened")
    #   GPIO.output(led[lckNum - 1], GPIO.HIGH)
    #   sleep(1)
    #   GPIO.output(led[lckNum - 1], GPIO.LOW)

class Main(QWidget):
    
    switch_window = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()

        main_layout = QGridLayout()
        
        button = {}
        for i in range(0,4):
            button[i] = QPushButtonNumber(str(i+1))
            font = button[i].font()
            font.setPointSize(40)
            # button[i].setFont(font)
            # button[i].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button[i].clicked.connect(lambda state, num = i+1 : self.number_button(num))
            button[i].setStyleSheet("""
                                    QPushButton{
                                        color: white;
                                        background-color: #00A5FF;
                                        border: 0;
                                        border-radius: 20px;
                                    }
                                    QPushButton:hover { background-color: #00b9ff; }
                                    """)
            
            x, y = divmod(i, 2)
            main_layout.addWidget(button[i], x, y)
        
        self.setLayout(main_layout)
        self.resize(400, 400)
        
    def number_button(self, num):
        self.switch_window.emit(num)
        
class Widget(QWidget):
    
    switch_window = pyqtSignal(int)
    
    def __init__(self, number):
        super().__init__()

        main_layout = QFormLayout()
        
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Set your password")
        self.password.setEchoMode(QLineEdit.Password);
        
        check_button = QPushButton("check")
        check_button.clicked.connect(lambda state, num = number : self.check_button(number))
        
        main_layout.addRow("password: ", self.password)
        main_layout.addRow(check_button)
        
        self.setLayout(main_layout)
        self.resize(400, 400)
        
    def check_button(self, num):
        password = self.password.text()
        self.password.setText("")
        if(password != ""):
            print(num, password)
            set_GPIO()
            server(num, password)

class QPushButtonNumber(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 20)
        font.setBold(True)
        self.setFont(font)
        
        
class Controller:
    def __init__(self):
        pass
    
    def show_main(self):
        self.main = Main()
        self.main.switch_window.connect(self.show_widget)
        self.main.show()
        
    def show_widget(self, number):
        self.widget = Widget(number)
        self.widget.show()
        
def main_app():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())
        

if __name__ == '__main__':
    main_app()