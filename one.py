import sys
from PyQt5 import QtWidgets as qwt                           #basicly every GUI objects
from PyQt5 import QtCore as qtc                              #low level stuff like signals etc.
from PyQt5 import QtGui as qtg                               #fonts graphical stuff etc.
import time
import os
import datetime
import logging
import logs

logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

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
            logging.info(f"Mamy {i}")
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

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)


         self.password_input = qwt.QLabel('')


         self.number7 = qwt.QPushButton('7')
         self.number8 = qwt.QPushButton('8')
         self.number9 = qwt.QPushButton('9')

         self.button_back_2 = qwt.QPushButton('Back')
         self.button_back_2.clicked.connect(self.switch_to_first)

         layout_second = qwt.QHBoxLayout()
         layout_second.addWidget(self.password_input)
         layout_second.addWidget(self.number7)
         layout_second.addWidget(self.number8)
         layout_second.addWidget(self.number9)

         layout_second.addWidget(self.button_back_2)

         self.setLayout(layout_second)

         self.number7.clicked.connect(self.push7)

         self.number8.clicked.connect(self.push8)
         #self.number9.clicked.connect(push9)



    def push7(self):
        if (len(self.password_input.text())<=5):
            self.number += '7'
            self.password_input.setText(self.number)
            self.password_input.show()
            self.checkPassword()

    def push8(self):
        if (len(self.password_input.text())<=5):
            self.number += '8'
            self.password_input.setText(self.number)
            self.checkPassword()
            self.password_input.show()


    def checkPassword(self):

        password_input=self.password_input.text()
        print(password_input)

        if (password_input == ('777888')):
            #qwt.QMessageBox.information(self,'siepr','asa')
            self.switch_to_third()



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


class ThirdWindow(qwt.QWidget):

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)


         self.haha = qwt.QLabel('haha')

         self.button_done = qwt.QPushButton('PERMISSION GRANTED')           #show message and after 4 sec go back
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
        self.writeLog()
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(0,50)
        self.first_window.show()
        self.close()


    def writeLog(self):
        data = [0,0,999]
        try:
            now = datetime.datetime.now()
            dir_path = os.path.dirname(os.path.realpath(__file__)) ## na raspberce będzie działac ale na windowsie nie

            path = "C:/Users/mjszo/Desktop/SmartLockLog-{}.txt".format(now.strftime("%B 20%y"))
            print(dir_path)
            file = open(path, mode='a+')

            dataToFile = now.strftime("20%y.%m.%d  %H:%M")
            if (data[0] == 0 and data[1] == 0 and data[2] == 999):
                file.writelines("{}  Access denied. Unknown user.\n".format(dataToFile))
            elif (data[0] == 0 and data[1] == 999 and data[2] == 0):
                file.writelines("{}  Access denied. Wrong code\n".format(dataToFile))
            elif data[0] == 1:
                file.writelines("{}  Access granted. Used userID={}\n".format(dataToFile, data[2]))
            elif data[0] == 2:
                file.writelines("{}  Access granted. Correct code\n")
            else:
                pass

            file.close()
        except:
            pass













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