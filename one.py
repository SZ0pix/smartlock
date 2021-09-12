#QT libraries
from PyQt5 import QtWidgets as qwt                           #basicly every GUI objects
from PyQt5 import QtCore as qtc                              #low level stuff like signals etc.
from PyQt5 import QtGui as qtg                               #fonts graphical stuff etc.
from PyQt5 import uic



#python libraries
import time
import os
import datetime
import logging
import sys
#python files
import logs
import logslogging

data = [0,0,999]

Ui_AccessGranted, baseClass = uic.loadUiType("C:/Users/mjszo/Desktop/1/acces.ui")
Ui_Keyboard, baseClass = uic.loadUiType("C:/Users/mjszo/Desktop/1/keyboard.ui")
#logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

logger2 = logging.getLogger(__name__)

HEIGHT = 640                                                    #standard window size
WIDTH = 1000
PASSCODE = '777888'                                             #password

endSig = qtc.pyqtSignal()



class SerialCom(qtc.QRunnable):
    def __init__(self):
        super().__init__()
    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(int)


    def run(self):
        i = 0
        while(True):
            i += 1
            time.sleep(1)
            logger2.warning(f"Mamy {i}")
            #self.progress.emit(i+1)
        #self.finished.emit()



class MainWindow(qwt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## Start code here
        time.sleep(1)
        self.switch_to_first()
        self.runTask()

    def switch_to_first(self):
         self.first_window = FirstWindow()
         self.first_window.resize(WIDTH, HEIGHT)
         self.first_window.setWindowTitle('First')
         self.first_window.move(0, 50)
         self.first_window.show()

    def screenSaver(self):
        self.tmscs = qtc.QTimer()  # one shot timer for 60 seconds
        self.tmscs.setSingleShot(True)
        self.tmscs.timeout.connect(self.switch_to_first)

        self.tmr1.start(4000)

    def runTask(self):
        pool = qtc.QThreadPool.globalInstance()
        runnalbe = SerialCom()
        pool.start(runnalbe)



    #def runLongTask(self):
    #    self.thread = qtc.QThread()
    #    self.serialcom  = SerialCom()
    #    self.serialcom.moveToThread(self.thread)

    #    self.thread.started.conntect(self.serialcom.taks)
    #    self.serialcom.finished.connect(self.thread.quit)
    #    self.serialcom.finished.connect(self.serialcom.deleteLater)
    #    self.thread.finished.connect(self.thread.deleteLater)
    #    self.serialcom.progress.connect(self.reportProgress)
    #    self.thread.start()




class FirstWindow(qwt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## Start code here

        self.setWindowFlags(flags)
        self.resize(WIDTH, HEIGHT)
        self.button_one = qwt.QPushButton('Start')
        self.button_one.clicked.connect(self.switch_to_second)

        layout = qwt.QFormLayout()
        self.setLayout(layout)
        layout.addRow(self.button_one)


        ##End code here

    def switch_to_second(self):
        self.second_window = SecondWindow()
        self.second_window.move(0,50)
        self.second_window.resize(WIDTH, HEIGHT)
        self.second_window.show()
        self.close()








class SecondWindow(qwt.QWidget):
    number = ''
    var1=0

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.ui = Ui_Keyboard()
        self.ui.setupUi(self)
        self.checkLabel()
        #self.setWindowFlags(flags)
        #self.ui.button_key1.clicked.connect(self.push1)
        #self.ui.button_key2.clicked.connect(self.push2)
        #self.ui.button_key3.clicked.connect(self.push3)
        #self.ui.button_key4.clicked.connect(self.push4)
        #self.ui.button_key5.clicked.connect(self.push5)
        #self.ui.button_key6.clicked.connect(self.push6)
        self.ui.button_key7.clicked.connect(self.push7)
        self.ui.button_key8.clicked.connect(self.push8)
        #self.ui.button_key9.clicked.connect(self.push9)
        #self.ui.button_key0.clicked.connect(self.push0)
        self.ui.button_keyBack.clicked.connect(self.switch_to_first)


    def checkLabel(self):
        if (len(self.number)==0):
            self.ui.label_key.setText("PASSWORD")  # show message and after 4 sec go back
        elif (len(self.number)==1):
            self.ui.label_key.setText("*")
        elif (len(self.number)==2):
            self.ui.label_key.setText("* *")
        elif (len(self.number)==3):
            self.ui.label_key.setText("* * *")
        elif (len(self.number)==4):
            self.ui.label_key.setText("* * * *")
        elif (len(self.number)==5):
            self.ui.label_key.setText("* * * * *")
        elif (len(self.number)>=6):
            self.ui.label_key.setText("* * * * * *")

        #self.ui.button.setFlat(True)

        #self.password_input = qwt.QLabel('')



        #layout_second = qwt.QHBoxLayout()
        #layout_second.addWidget(self.password_input)
        #layout_second.addWidget(self.number7)
        #layout_second.addWidget(self.number8)
        #layout_second.addWidget(self.number9)

        #layout_second.addWidget(self.button_back_2)

        #self.setLayout(layout_second)

        #self.number7.clicked.connect(self.push7)

        #self.number8.clicked.connect(self.push8)
        #self.number9.clicked.connect(push9)



    def push7(self):
        if (len(self.number)<=5):
            self.number += '7'
            print(self.number)
            self.checkLabel()
            self.checkPassword()

    def push8(self):
        if (len(self.number) <= 5):
            self.number += '8'
            print(self.number)
            self.checkLabel()
            self.checkPassword()


    def checkPassword(self):
        password_input=self.number
        if (password_input == ('777777')):
            #qwt.QMessageBox.information(self,'siepr','asa')
            self.switch_to_third()
        elif (password_input == ('888888')):
            #qwt.QMessageBox.information(self,'siepr','asa')
            self.switch_to_fourth()


    def switch_to_first(self):                                  #go back to window 1
        self.first_window = FirstWindow()
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(0,50)
        self.first_window.show()
        self.close()

    def switch_to_third(self):

        self.third_window = ThirdWindow()
        self.third_window.resize(WIDTH, HEIGHT)
        self.third_window.move(0,50)
        self.third_window.show()
        self.close()

    def switch_to_fourth(self):

        self.fourth_window = FourthWindow()
        self.fourth_window.resize(WIDTH, HEIGHT)
        self.fourth_window.move(0,50)
        self.fourth_window.show()
        self.close()


class ThirdWindow(baseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AccessGranted()
        self.ui.setupUi(self)
        self.setWindowFlags(flags)
        self.ui.button.setFlat(True)
        self.ui.button.clicked.connect(self.stopTimer)              #or if button is pushed
        self.Win()

    def Win(self):
        self.ui.button.setText("ACCESS GRANTED")  # show message and after 4 sec go back
        self.tmr1 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr1.setSingleShot(True)
        self.tmr1.timeout.connect(self.switch_to_first)
        self.tmr1.start(4000)

    def stopTimer(self):
        self.tmr1.stop()
        self.switch_to_first()

    def switch_to_first(self):
        self.first_window = FirstWindow()
        logslogging.writeLog2(data)
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(0,50)
        self.first_window.show()
        self.close()


class FourthWindow(ThirdWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Win()

    def Win(self):
        self.ui.button.setText("ACCESS DENIED")  # show message and after 4 sec go back
        self.tmr2 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr2.setSingleShot(True)
        self.tmr2.timeout.connect(self.switch_to_first)
        self.tmr2.start(8000)

    def stopTimer(self):
        self.tmr2.stop()
        self.switch_to_first()

    def switch_to_first(self):
        self.first_window = FirstWindow()
        #logslogging.writeLog2(data)
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(0, 50)
        self.first_window.show()
        self.close()


class ScreenSaver(qwt.QWidget):

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)


         self.haha = qwt.QLabel('wygaszacz')

         self.button_done = qwt.QPushButton('Wygaszacz')           #show message and after 4 sec go back
         self.button_done.clicked.connect(self.switch_to_first)             #or if button is pushed
         layout_s2econd = qwt.QHBoxLayout()
         layout_s2econd.addWidget(self.haha)
         layout_s2econd.addWidget(self.button_done)

         self.setLayout(layout_s2econd)

         self.tmr1 = qtc.QTimer()                                           #one shot timer for 4 seconds
         self.tmr1.setSingleShot(True)
         self.tmr1.timeout.connect(self.switch_to_first)
         self.tmr1.start(4000)

    def switch_to_first(self):                                              #switch window
        self.first_window = FirstWindow()
        #logslogging.writeLog2(data)
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(0,50)
        self.first_window.show()
        self.close()









if __name__ == '__main__':
    # ser=serial.Serial('/dev/ttyACM0',9600,timeout=1)
    # ser.flush()
    # while True :
    #
    #	if  ser.in_waiting>0:
    #		zmn=ser.readline().decode('utf-8').rstrip()
    #		zmn=int(zmn)
    #		if zmn==9:
    #			print(zmn)
    #			liczba=random.randint(1,3)
    #			print(liczba)
    #			ser.write(str(liczba).encode('utf-8'))


    app = qwt.QApplication(sys.argv)
    w = MainWindow(windowTitle='dupa dupa')
    sys.exit(app.exec_())                                        #starts eventloop
    #dane = [0, 0, 999]
    #print('doszliśmy')
    #logs.writeLog(dane)