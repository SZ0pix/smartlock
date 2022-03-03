# QT libraries
from PyQt5 import QtWidgets as qwt  # basicly every GUI objects
from PyQt5 import QtCore as qtc  # low level stuff like signals etc.
from PyQt5 import QtGui as qtg  # fonts graphical stuff etc.
from PyQt5 import uic

# python libraries
import time
import random
import os
import datetime
import logging
import sys
import serial
# python files
#import logs sprawdzic czy bez tego dziala
from files import logslogging
from files import logsloggingenroll
from files import communication
from files import passwords
from files import mail


data = [9, 3, 0]
photoPath = "photos"

Ui_Stacked, baseClass = uic.loadUiType("graphic/stacked1.ui")

logging.basicConfig(format="%(message)s", level=logging.INFO)

flags = qtc.Qt.WindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)

logger2 = logging.getLogger(__name__)
HEIGHT = 600        #       standard window sizex
WIDTH = 1024
POSITION_X = 0      #       position on screen x
POSITION_Y = 0     #       position on screen y
TIMER = 5000        #       default slideshow delay (in ms)
INTERVAL = 1        #       default passcode generator interval (in months)
SETTINGS_PASSCODE = '111118'
MECHANICS_PASSCODE = '8816'
global GLOBALTRIGGER
GLOBALTRIGGER = False


class Signals(qtc.QObject):                           #signals used in code
    updateTimeSignal = qtc.pyqtSignal(str, str, bool)       #for RTC clock
    incomingDataSignal = qtc.pyqtSignal(str)                #for communication with Arduino board

class Clock_thread(qtc.QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = Signals()                                  # initiate signals
        self.start_month = datetime.datetime.today().strftime('%m')     # needed for auto mode - will be overwritten
        self.start_month = int(self.start_month)                        # change var type
        self.interwal = INTERVAL                                        # create local var with value of global var INTERVAL

    def run(self):                                                      #main fuction of thred
        while (True):
            time.sleep(1)  # loop delay
            self.update_date = datetime.datetime.today().strftime('%A, %d.%m')  # take current date and time
            self.update_time = datetime.datetime.today().strftime('%H:%M:%S')
            self.new_month = datetime.datetime.today().strftime('%m')
            self.new_month = (int(self.new_month))

            self.diff = (abs(self.start_month - self.new_month))    # difference between old month in memory and current
            if (self.diff == self.interwal) or (
                    self.diff == (12 - self.interwal)):             # checks if difference matches interval
                self.start_month = self.new_month                   # overwrite start_month variable
                self.signals.updateTimeSignal.emit(self.update_time, self.update_date, True)    #emit signal with date and wheter automode
                                #should generate new passcode (based on set interval)
                logslogging.configure()     #change logs file names
            else:
                self.signals.updateTimeSignal.emit(self.update_time, self.update_date, False)

class Communication_thread(qtc.QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = Signals()                                #initiate signals
        print('Running. Press CTRL-C to exit.')
        self.arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=0.3)
        
    def run(self):    #main function of thread
        if self.arduino.isOpen():
            print("{} connected!".format(self.arduino.port))
            while (True):
                if  self.arduino.inWaiting()>0: 
                    answer=str(self.arduino.readline().decode('utf-8').rstrip())
                    print(answer)
                    print("Przyszło")
                    self.signals.incomingDataSignal.emit(answer)
                    self.arduino.flushInput() #remove data after reading
        else:
            print("zepsulosie")

    def write(self, msg):
        self.arduino.flushInput() #remove data after reading
        self.arduino.write(str(msg).encode())
        print("Poszło")
            
class Mail_thread(qtc.QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = Signals()                #initiate signals

    def run(self):
    
        while(True):
            time.sleep(1)                       #delay for optimizing GUI
            global GLOBALTRIGGER                #checks value of global variable (set earlier)
            if GLOBALTRIGGER==True:
                kod=passwords.check_current()   #if var is true thread checks passords and sends mail to users with it
                mail.sendmail(kod)
                GLOBALTRIGGER = False           #set variable to flase

class MainWindow(qwt.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.old_date = "30.02"                 #create cariable and give it value
        self.sendNow = False
        self.ui = Ui_Stacked()                  #load ui
        self.ui.setupUi(self)
        #self.setWindowFlags(flags)
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle('SmartLock_GUI')    #set title of window
        self.move(POSITION_X, POSITION_Y)       #set starting position on screen
        self.auto = AUTO                        #make local varsions of variables
        self.timerVal = TIMER
        self.start()                            #set start widget
        self.initiate()                         #set buttons and sliders connectiotns
        self.ui.button_start.setText("PRESS TO START")          #set label text on start button
        self.run_task()                          #run threads
        time.sleep(0.5)                         #delay for optimizing GUI
        self.show()                             #showing GUI
        self.arduino = False
        self.number=''
        
    @qtc.pyqtSlot(str, str, bool)               #slot for signal
    def printCurrentDataTime(self, time, date, signal):
        self.ui.label_hour_start.setText(time)          #recive current time and date
        self.ui.label_date_start.setText(date)

        if signal and self.auto:                        #if auto mode is ON and signal of interval
            self.generate()                             #change password

    @qtc.pyqtSlot(str)                          #slot for signal
    def trigerchange(self, answer):
        if(answer[6]==">"):
            out=int(answer[5])
        elif(answer[7]==">"):
            out=int(answer[5]+answer[6])
        elif(answer[8]==">"):
            out=int(answer[5]+answer[6]+answer[7])
        data=[int(answer[1]),int(answer[3]),out]
        text = communication.analize(data)
        self.data=data
        if (data[0] == 1 and data[1] == 0):
            self.tmr4.stop()
            self.ui.button_access.setText("ACCESS GRANTED")
            self.arduino=True
            self.access_granted()
        if (data[0] == 0 and data[1] == 0 and data[2] == 9):
            self.tmr4.stop()
            self.ui.button_access.setText("ACCESS DENIED")
            self.arduino=True
            self.access_denied()
        if len(str(text))>4:
            self.ui.label_instruction_enroll.setText(text)
        if (data[1] == 4):
            self.fill()
        else:
            pass

    def run_task(self):
        self.pool = qtc.QThreadPool.globalInstance()                      #creat pool for threads
        self.runnalbe = Clock_thread()                               #create instances of threads
        self.worke = Communication_thread()
        self.wor = Mail_thread()

        self.runnalbe.signals.updateTimeSignal.connect(self.printCurrentDataTime)       #connection of signals and slots
        self.worke.signals.incomingDataSignal.connect(self.trigerchange)

        self.pool.start(self.worke)              #starting threads
        self.pool.start(self.runnalbe)
        self.pool.start(self.wor)

    def initiate(self):                         #all buttons and sliders connections
        #       keyboard
        self.ui.button_key1.clicked.connect(lambda: self.push(1))
        self.ui.button_key2.clicked.connect(lambda: self.push(2))
        self.ui.button_key3.clicked.connect(lambda: self.push(3))
        self.ui.button_key4.clicked.connect(lambda: self.push(4))
        self.ui.button_key5.clicked.connect(lambda: self.push(5))
        self.ui.button_key6.clicked.connect(lambda: self.push(6))
        self.ui.button_key7.clicked.connect(lambda: self.push(7))
        self.ui.button_key8.clicked.connect(lambda: self.push(8))
        self.ui.button_key9.clicked.connect(lambda: self.push(9))
        self.ui.button_key0.clicked.connect(lambda: self.push(0))
        self.ui.button_back_key.clicked.connect(self.start)
        self.ui.button_cancel_key.clicked.connect(self.cancel)
        self.ui.button_set_key.clicked.connect(self.settings)
        #       screensaver
        self.ui.button_screen.clicked.connect(self.stopTMR3)
        #       start
        self.ui.button_start.clicked.connect(self.go_to_keyboard)
        #       access_granted
        self.ui.button_access.clicked.connect(self.stopTMR1)
        #       settings
        self.ui.button_1_set.clicked.connect(self.start_enroll)
        self.ui.button_2_set.clicked.connect(self.logs)
        self.ui.button_3_set.clicked.connect(self.set_timer)
        self.ui.button_4_set.clicked.connect(self.menu_password)
        self.ui.button_5_set.clicked.connect(self.turn_off)
        self.ui.button_back_set.clicked.connect(self.go_to_keyboard)
        #       logs
        self.ui.button_back_logs.clicked.connect(self.settings_menu)
        self.ui.slider_month_logs.valueChanged.connect(self.updateLog)
        self.ui.slider_year_logs.valueChanged.connect(self.updateLog)
        #       enroll
        self.ui.button_finish_enroll.clicked.connect(self.finish_enroll)
        self.ui.button_clear_enroll.clicked.connect(self.cancel2)
        self.ui.button_A.clicked.connect(lambda: self.push2('A'))
        self.ui.button_B.clicked.connect(lambda: self.push2('B'))
        self.ui.button_C.clicked.connect(lambda: self.push2('C'))
        self.ui.button_D.clicked.connect(lambda: self.push2('D'))
        self.ui.button_E.clicked.connect(lambda: self.push2('E'))
        self.ui.button_F.clicked.connect(lambda: self.push2('F'))
        self.ui.button_G.clicked.connect(lambda: self.push2('G'))
        self.ui.button_H.clicked.connect(lambda: self.push2('H'))
        self.ui.button_I.clicked.connect(lambda: self.push2('I'))
        self.ui.button_J.clicked.connect(lambda: self.push2('J'))
        self.ui.button_K.clicked.connect(lambda: self.push2('K'))
        self.ui.button_L.clicked.connect(lambda: self.push2('L'))
        self.ui.button_M.clicked.connect(lambda: self.push2('M'))
        self.ui.button_N.clicked.connect(lambda: self.push2('N'))
        self.ui.button_O.clicked.connect(lambda: self.push2('O'))
        self.ui.button_P.clicked.connect(lambda: self.push2('P'))
        self.ui.button_R.clicked.connect(lambda: self.push2('R'))
        self.ui.button_S.clicked.connect(lambda: self.push2('S'))
        self.ui.button_T.clicked.connect(lambda: self.push2('T'))
        self.ui.button_U.clicked.connect(lambda: self.push2('U'))
        self.ui.button_W.clicked.connect(lambda: self.push2('W'))
        self.ui.button_Y.clicked.connect(lambda: self.push2('Y'))
        self.ui.button_Z.clicked.connect(lambda: self.push2('Z'))
        self.ui.button_Space.clicked.connect(lambda: self.push2(' '))
        #       menu_password
        self.ui.button_1_menu.clicked.connect(self.generate)
        self.ui.button_2_menu.clicked.connect(self.change_mode)
        self.ui.button_back_menu.clicked.connect(self.settings_menu)
        #       delay
        self.ui.button_set_delay.clicked.connect(self.send_delay)
        self.ui.button_back_delay.clicked.connect(self.settings_menu)
        self.ui.slideshow_delay_slider.valueChanged.connect(self.set_timer)
        self.ui.relay_delay_slider.valueChanged.connect(self.set_timer)

    def turn_off(self):
        sys.exit()

    def change_mode(self):
        if self.auto == True:           #toggle button for auto mode
            self.auto = False
            self.update_button()        #label update
        else:
            self.auto = True
            self.update_button()        #label update

    def update_button(self):
        if self.auto == False:
            self.ui.button_2_menu.setText("AUTO MODE: OFF")         #update label
            self.ui.button_1_menu.show()                            #show additional button
        else:
            self.ui.button_2_menu.setText("AUTO MODE: ON")
            self.ui.button_1_menu.hide()

#   MENU PASSWORD
    def generate(self):
        self.today = self.update_date = datetime.datetime.today().strftime('%d.%m')             #get current date
        if (self.old_date != self.today):                                                       #checks when last time password was chanegd
            passwords.newpass()                                                                 #new passord
            self.old_date = self.today                                                          #overwrite date of last password change
            current_password = passwords.check_current()                                        #get current (new) password
            self.ui.label_menu_password.setText("CURRENT PASSWORD: " + passwords.check_current())       #update label
            logslogging.write_password(passwords.check_current())                                        #creat log
            global GLOBALTRIGGER
            GLOBALTRIGGER = True                                                                #set global var to sending mail
        else:
            self.tmr2 = qtc.QTimer()                            #one shot timer for 4 seconds
            self.tmr2.setSingleShot(True)
            self.tmr2.timeout.connect(self.fix_label)
            self.tmr2.start(2000)
            self.ui.label_menu_password.setText("PASSWORD CAN'T BE CHANGED")       #update label

    def fix_label(self):
        self.ui.label_menu_password.setText("CURRENT PASSWORD: " + passwords.check_current())   #update Label

    def menu_password(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.menu_password)       #set current widget
        current_password = passwords.check_current()                        #check password
        self.update_button()                                                #check if auto mode in ON
        self.ui.label_menu_password.setText("CURRENT PASSWORD: " + current_password)

#   SET TIMER
    def set_timer(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.delay)           #set current widget
        value1 = self.ui.slideshow_delay_slider.value()                 #get values from sliders
        value2 = self.ui.relay_delay_slider.value()
        self.ui.slideshow_delay.setText(f"SLIDESHOW DELAY VALUE: {value1}s")    #set label text
        self.ui.relay_delay.setText(f"RELAY DELAY VALUE: {value2}s")

    def send_delay(self):
        self.timerVal=int(self.ui.slideshow_delay_slider.value())*1000  #set values and change widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings)

#   ENROLL
    def start_enroll(self):
        
        self.ui.label_data_enroll.setVisible(False)     #hide widgets
        self.ui.scrollArea_2.setVisible(False)        
        self.ui.button_clear_enroll.setVisible(False)
        self.ui.label_instruction_enroll.setText('Press finger')
        self.ui.stackedWidget.setCurrentWidget(self.ui.enroll)      #set current widget
        self.name = ''                                      #clear label text
        self.check_name()                                   #update label
        self.worke.write("<9;9;0>")                         #-----------------------------------------
        communication.analize(data)               
        self.tmr6 = qtc.QTimer()                            #one shot timer for 30 seconds
        self.tmr6.setSingleShot(True)
        self.tmr6.timeout.connect(self.break_enroll)
        self.tmr6.start(60000)

    def check_name(self):
        if (len(self.name) == 0):
            self.ui.label_data_enroll.setText("YOUR NAME")  # show message and after 4 sec go back
        else:
            self.ui.label_data_enroll.setText(self.name)

    def break_enroll(self):
        self.tmr6.stop()                #stop timer
        self.settings_menu()

    def finish_enroll(self):
        self.tmr6.stop()                #stop timer
        name = self.name
        print(self.data[2])
        if (self.data[1] == 4):
            logsloggingenroll.write_names(self.data[2], name)
        self.start()

    def fill(self):             #enables poles for entering data if enroll was succesful
        self.ui.label_data_enroll.setVisible(True)
        self.ui.scrollArea_2.setVisible(True)
        self.ui.button_clear_enroll.setVisible(True)

    def push2(self, sign):              # letter keyboard
        if (len(self.name) <= 30):
            self.name += str(sign)
            self.check_name()            # update label

    def cancel2(self):
        if (len(self.name) >= 1):
            temp_name = list(self.name)  # create list that is equal to current input
            var2 = len(self.name) - 1  # check length
            temp_name[var2] = ''  # set last cell in list as nothing
            self.name = ''.join(temp_name)  # recreate string and sign it to self.name
            self.check_name()  # update label

#   START
    def start(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.start)       #set widget
        self.tmr4 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr4.setSingleShot(True)
        self.tmr4.timeout.connect(self.switch_to_saver)
        self.tmr4.start(5000)
                        # or if button is pushed --> check go_to_keyboard funtion

#   KEYBOARD
    def go_to_keyboard(self):
        self.ui.button_set_key.show()
        self.number = ''                                                        #var for stocking user input
        self.keyboard = True
        self.check_label()                                                       #update label with variables
        self.ui.stackedWidget.setCurrentWidget(self.ui.keyboard_key)            #set widget
        self.tmr4.stop()        #stop screensaver timer
        self.arduino = False

    def check_label(self):
        if (len(self.number) == 0 and self.keyboard==True):
            self.ui.label_key.setText("ENTER PASSWORD")  #update label with number of signes passed by user
        elif (len(self.number) == 0 and self.keyboard==False):
            self.ui.label_key.setText('SETTINGS CODE')
        elif (len(self.number) == 1):
            self.ui.label_key.setText("X")
        elif (len(self.number) == 2):
            self.ui.label_key.setText("X  X")
        elif (len(self.number) == 3):
            self.ui.label_key.setText("X  X  X")
        elif (len(self.number) == 4):
            self.ui.label_key.setText("X  X  X  X")
        elif (len(self.number)==5 and self.keyboard==False):
            self.ui.label_key.setText("X  X  X  X  X")
        elif (len(self.number)>=6 and self.keyboard==False):
            self.ui.label_key.setText("X  X  X  X  X  X")

    def push(self, sign):
        if (len(self.number) <= 3 and self.keyboard==True):     #counts passed signes by user
            self.number += str(sign)
            self.check_label()           #updates label
            self.check_password()        #checks password
        elif (len(self.number) <= 5 and self.keyboard == False):  # counts passed signes by user
            self.number += str(sign)
            self.check_label()  # updates label
            self.check_password()  # checks password

    def cancel(self):
        if (len(self.number) >= 1):
            temp_number = list(self.number)  # create list that is equal to current input
            var1 = len(self.number) - 1  # check length
            temp_number[var1] = ''  # set last cell in list as nothing
            self.number = ''.join(temp_number)  # recreate string and sign it to self.number
            self.check_label()  # update label

    def check_password(self):
        password_input = self.number            #assign input to variable
        self.PASSCODE = passwords.check_current()
        if ((password_input == (self.PASSCODE) or password_input == '8816' )and self.keyboard==True):
            self.access_granted()
        elif ((len(password_input) == 4) and (password_input != self.PASSCODE) and self.keyboard==True):
            self.access_denied()
        elif (password_input == (SETTINGS_PASSCODE) and self.keyboard==False):
            self.ui.stackedWidget.setCurrentWidget(self.ui.settings)
        elif ((len(password_input) == 6) and password_input != (SETTINGS_PASSCODE) and self.keyboard==False):
            self.start()

    def access_denied(self):
        self.ui.button_access.clicked.connect(self.stopTMR1)  # or if button is pushed
        if self.arduino==False:
            self.data = [0, 999, 0]
        self.status()           #update labels

    def access_granted(self):
        self.ui.button_access.clicked.connect(self.stopTMR1)  # or if button is pushed
        if self.arduino==False:
            self.data = [2, 999, 0]
        self.status()          #update labels

    def status(self):           #information about veryfication
        if (self.data[0] == 2 or self.data[0] == 1):
            self.ui.button_access.setText("ACCESS GRANTED")  # show message and after 4 sec go back
            if self.arduino==False:
                self.worke.write(f"<1;0;{str(self.ui.relay_delay_slider.value())}>")
                self.arduino=True
        elif self.data[0] == 0:
            self.ui.button_access.setText("ACCESS DENIED")  # show message and after 4 sec go back
        self.ui.stackedWidget.setCurrentWidget(self.ui.access_granted)
        if self.number=='8816':
            logslogging.write_log_mechanic()
            self.number=''
        else:
            logslogging.write_log(self.data)
        self.tmr1 = qtc.QTimer()  # one shot timer for 4 seconds
        self.tmr1.setSingleShot(True)
        self.tmr1.timeout.connect(self.start)
        self.tmr1.start(4000)

    def stopTMR1(self):
        self.tmr1.stop()                #stop timer
        self.start()                    #switch to start

#   SETTINGS
    def settings(self):
        self.ui.button_set_key.hide()
        self.ui.label_key.setText('SETTINGS CODE')
        self.keyboard=False
        self.check_label()                                                       #update label with variables

    def settings_menu(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings)

#   LOGS
    def updateLog(self):
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                  9: "September", 10: "October", 11: "November", 12: "December"}                # match postions of slider wth months
        self.ui.slider_year_logs.setMaximum(int(datetime.datetime.today().strftime("%Y")))      # set slider limits for years
        number = self.ui.slider_month_logs.value()                      # get values
        searched_month = months[number]
        try:
            line = logslogging.read_log(searched_month, self.ui.slider_year_logs.value())       #read logs from file
            text = ""
            for i in line:
                text += i + '\n'
            self.ui.label_logs.setText(text)                                                    #show logs in box
            self.ui.current_date_logs.setText(f"{searched_month}.{self.ui.slider_year_logs.value()}")   #update label

        except:
            text = "ERROR: NO LOGS FOUND FOR THIS MONTH"
            self.ui.label_logs.setText(text)
            self.ui.current_date_logs.setText(f"{searched_month}.{self.ui.slider_year_logs.value()}")

    def logs(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.logs)            #change current label
        self.updateLog()

#   SCREEN SAVER
    def switch_to_saver(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.screensaver_screen)      #switch widget
        self.tmr3 = qtc.QTimer()  # one shot timer for 4 seconds#
        self.tmr3.setSingleShot(True)  # start timer and in case of timeout change photo
        self.tmr3.timeout.connect(self.changePic)
        self.loadPictures()  # load pictures from path
        self.shotTimer()  # initialise timer in shot mode
        self.changePic()  # initialise picture rotation

    def stopTMR3(self):
        self.tmr3.stop()            #stop timer
        self.start()                #switch to start screen

    def loadPictures(self):
        self.pixlist = {}  # create dictionary
        self.number_of_photos = len([file for file in os.listdir(photoPath) if
                           os.path.isfile(os.path.join(photoPath, file))])  # count number of files(photos) in folder
        for i in range(1, self.number_of_photos + 1):
            self.pixlist["pixmap" + str(i)] = qtg.QPixmap(
                f"{photoPath}/" + str(i) + ".jpg")  # create dictionary and load pictures to pixmap variables#

    def shotTimer(self):
        self.tmr3.start(self.timerVal)  # start timer and in case of timeout change photo

    def changePic(self):
        pic = random.randint(1, self.number_of_photos)  # draw number from 1 to the number of loaded photos
        self.ui.label_screen.setPixmap(qtg.QPixmap(self.pixlist[f"pixmap{pic}"]))  # set photo to label
        self.shotTimer()  # relaunch timer


if __name__ == '__main__':
    AUTO = True
    app = qwt.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())  # starts eventloop