#QT libraries
from PyQt5 import QtWidgets as qwt                           #basicly every GUI objects
from PyQt5 import QtCore as qtc                              #low level stuff like signals etc.
from PyQt5 import QtGui as qtg                               #fonts graphical stuff etc.
from PyQt5 import uic



#python libraries
import time
import random
import os
import datetime
import logging
import sys
#python files
import logs
import logslogging

data = [0,0,999]
photoPath="C:/Users/mjszo/OneDrive/Pulpit/1/photos"
uiPath="C:/Users/mjszo/OneDrive/Pulpit/1"

Ui_AccessGranted, baseClass = uic.loadUiType(f"{uiPath}/access_granted.ui")
Ui_Keyboard,baseClass = uic.loadUiType(f"{uiPath}/keyboard.ui")
Ui_Start,baseClass = uic.loadUiType(f"{uiPath}/access.ui")
Ui_ScreenSaver,baseClass = uic.loadUiType(f"{uiPath}/screensaver.ui")
Ui_Settings,baseClass = uic.loadUiType(f"{uiPath}/settings.ui")
Ui_Main,baseClass = uic.loadUiType(f"{uiPath}/main.ui")

logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

logger2 = logging.getLogger(__name__)

HEIGHT = 600                                                    #standard window size
WIDTH = 1024
PASSCODE = '456322'                                             #password
POSITION_X = 0
POSITION_Y = 50
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
        #self.ui = Ui_Main()
        #self.ui.setupUi(self)
        #self.resize(WIDTH, HEIGHT)
        #self.setWindowFlags(flags)
        #self.move(POSITION_X, POSITION_Y)
        #self.show()
        time.sleep(1)
        self.switch_to_first()
        self.runTask()

    def switch_to_first(self):

         self.first_window = FirstWindow()
         self.first_window.resize(WIDTH, HEIGHT)
         self.first_window.setWindowTitle('First')
         self.first_window.move(POSITION_X,POSITION_Y)
         self.first_window.show()

    def screenSaver(self):
        self.tmscs = qtc.QTimer()  # one shot timer for 60 seconds
        self.tmscs.setSingleShot(True)
        self.tmscs.timeout.connect(self.switch_to_first)

        #self.tmr1.start(4000)

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
        self.ui = Ui_Start()
        self.ui.setupUi(self)
        self.setWindowFlags(flags)
        self.ui.button_start.setText("PRESS TO START")


        self.tmr4 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr4.setSingleShot(True)
        self.tmr4.timeout.connect(self.switch_to_saver)
        self.tmr4.start(5000)
        self.ui.button_start.clicked.connect(self.stopTimer)  # or if button is pushed

    def stopTimer(self):
        self.tmr4.stop()
        self.switch_to_second()

    def switch_to_second(self):
        #self.ui = Ui_Keyboard()
        #self.ui.setupUi(self)
        self.second_window = SecondWindow()
        self.second_window.show()
        self.second_window.move(POSITION_X,POSITION_Y)
        self.second_window.resize(WIDTH, HEIGHT)
        #time.sleep(2)
        self.close()

    def switch_to_saver(self):
        self.saver_window = ScreenSaver()
        self.saver_window.move(POSITION_X,POSITION_Y)
        self.saver_window.resize(WIDTH, HEIGHT)
        self.saver_window.show()
        self.close()

class SecondWindow(qwt.QWidget):
    number = ''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Keyboard()
        self.ui.setupUi(self)
        self.checkLabel()
        self.setWindowFlags(flags)
        self.ui.button_key1.clicked.connect(lambda : self.push(1))
        self.ui.button_key2.clicked.connect(lambda : self.push(2))
        self.ui.button_key3.clicked.connect(lambda : self.push(3))
        self.ui.button_key4.clicked.connect(lambda : self.push(4))
        self.ui.button_key5.clicked.connect(lambda : self.push(5))
        self.ui.button_key6.clicked.connect(lambda : self.push(6))
        self.ui.button_key7.clicked.connect(lambda : self.push(7))
        self.ui.button_key8.clicked.connect(lambda : self.push(8))
        self.ui.button_key9.clicked.connect(lambda : self.push(9))
        self.ui.button_key0.clicked.connect(lambda : self.push(0))
        self.ui.button_keyBack.clicked.connect(self.switch_to_first)
        self.ui.button_keyCancel.clicked.connect(self.cancel)
        self.ui.button_keySet.clicked.connect(self.settings)

    def checkLabel(self):
        if (len(self.number)==0):
            self.ui.label_key.setText("ENTER PASSWORD")  # show message and after 4 sec go back
        elif (len(self.number)==1):
            self.ui.label_key.setText("X")
        elif (len(self.number)==2):
            self.ui.label_key.setText("X X")
        elif (len(self.number)==3):
            self.ui.label_key.setText("X X X")
        elif (len(self.number)==4):
            self.ui.label_key.setText("X X X X")
        elif (len(self.number)==5):
            self.ui.label_key.setText("X X X X X")
        elif (len(self.number)>=6):
            self.ui.label_key.setText("X X X X X X")

    def push(self,sign):
        if (len(self.number)<=5):
            self.number += str(sign)
            print(self.number)
            self.checkLabel()
            self.checkPassword()

    def cancel(self):
        if (len(self.number)>=1):
            temp_number=list(self.number)               #create list that is equal to current input
            var1 = len(self.number) - 1                 #check length
            temp_number[var1]=''                        #set last cell in list as nothing
            self.number=''.join(temp_number)            #recreate string and sign it to self.number
            self.checkLabel()                           #update label

    def settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.resize(WIDTH, HEIGHT)
        self.settings_window.move(POSITION_X, POSITION_Y)
        self.close()
        self.settings_window.show()


        #var1=len(self.number)-1
        #temp_number = self.number
        #for i in range (var1):
        #    print(i)
        #    temp_number[i]='1'
        #temp_number[0]=self.number[0]
        #print(self.number)
        #print(temp_number)

        #print(type(self.number))
        #var1 = len(self.number)
        #print(var1)
        #print((str(self.number))[var1-1])
        #self.string[var1-1]=''
        #if(var1>=1):
        #    (str(self.number))[:-1]
        #    print(self.number)

    def checkPassword(self):
        password_input=self.number
        if (password_input == (PASSCODE)):
            self.switch_to_third()
        elif ((len(password_input) == 6) and (password_input != PASSCODE)):
            self.switch_to_fourth()

    def switch_to_first(self):                                  #go back to window 1
        self.first_window = FirstWindow()
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(POSITION_X,POSITION_Y)
        self.first_window.show()
        self.close()

    def switch_to_third(self):
        self.third_window = ThirdWindow()
        self.third_window.resize(WIDTH, HEIGHT)
        self.third_window.move(POSITION_X,POSITION_Y)
        self.third_window.show()
        self.close()

    def switch_to_fourth(self):
        self.fourth_window = FourthWindow()
        self.fourth_window.resize(WIDTH, HEIGHT)
        self.fourth_window.move(POSITION_X,POSITION_Y)
        self.fourth_window.show()
        self.close()

class ThirdWindow(baseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AccessGranted()
        self.ui.setupUi(self)
        self.setWindowFlags(flags)
        self.ui.button_access.setFlat(True)
        self.ui.button_access.clicked.connect(self.stopTimer)              #or if button is pushed
        self.Win()
        self.data=[2,999,0]

    def Win(self):
        self.ui.button_access.setText("ACCESS GRANTED")  # show message and after 4 sec go back
        self.tmr1 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr1.setSingleShot(True)
        self.tmr1.timeout.connect(self.switch_to_first)
        self.tmr1.start(4000)

    def stopTimer(self):
        self.tmr1.stop()
        self.switch_to_first()

    def switch_to_first(self):
        self.first_window = FirstWindow()
        logslogging.writeLog2(self.data)
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(POSITION_X,POSITION_Y)
        self.first_window.show()
        self.close()


class FourthWindow(ThirdWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Win()
        self.data = [0, 999, 0]

    def Win(self):
        self.ui.button_access.setText("ACCESS DENIED")  # show message and after 4 sec go back
        self.tmr2 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr2.setSingleShot(True)
        self.tmr2.timeout.connect(self.switch_to_first)
        self.tmr2.start(8000)

    def stopTimer(self):
        self.tmr2.stop()
        self.switch_to_first()

    def switch_to_first(self):
        self.first_window = FirstWindow()
        logslogging.writeLog2(self.data)
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(POSITION_X,POSITION_Y)
        self.first_window.show()
        self.close()


class SettingsWindow(qwt.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Settings()  # load UI form folder
        self.ui.setupUi(self)
        self.setWindowFlags(flags)  # get rid off frames
        self.ui.button_setBack.clicked.connect(self.switch_to_second)

    def switch_to_second(self):
        self.second_window = SecondWindow()
        self.second_window.move(POSITION_X,POSITION_Y)
        self.second_window.resize(WIDTH, HEIGHT)
        self.second_window.show()
        self.close()

class ScreenSaver(qwt.QWidget):
    timerVal=5000
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_ScreenSaver()      #load UI form folder
        self.ui.setupUi(self)
        self.setWindowFlags(flags)      #get rid off frames
        self.ui.button_screen.clicked.connect(self.switch_to_first)

        self.tmr3 = qtc.QTimer()  # one shot timer for 4 seconds

        self.loadPictures()             #load pictures from path
        self.shotTimer()                #initialise timer in shot mode
        self.changePic()                #initialise picture rotation


    def loadPictures(self):
        self.pixlist = {}               #create dictionary
        self.number = len([file for file in os.listdir(photoPath) if os.path.isfile(os.path.join(photoPath, file))])    #count number of files(photos) in folder
        for i in range(1, self.number + 1):
            self.pixlist["pixmap" + str(i)] = qtg.QPixmap(f"{photoPath}/" + str(i) + ".jpg")           #create dictionary and load pictures to pixmap variables

    def shotTimer(self):
        self.tmr3.setSingleShot(True)                       #start timer and in case of timeout change photo
        self.tmr3.timeout.connect(self.changePic)
        self.tmr3.start(self.timerVal)

    def changePic(self):
        pic = random.randint(1, self.number)                            #draw number from 1 to the number of loaded photos
        self.ui.label_screen.setPixmap(qtg.QPixmap(self.pixlist[f"pixmap{pic}"]))       #set photo to label
        self.shotTimer()                                            #relaunch timer

    def switch_to_first(self):
        self.first_window = FirstWindow()           #in case of touching one giant button for all window swithc to 1st
        self.first_window.resize(WIDTH, HEIGHT)
        self.first_window.move(POSITION_X,POSITION_Y)
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
    w = MainWindow()
    sys.exit(app.exec_())                                        #starts eventloop
    #dane = [0, 0, 999]
    #print('doszliśmy')
    #logs.writeLog(dane)