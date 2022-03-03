import smtplib
import datetime
from PyQt5 import QtCore as qtc                     #low level stuff like signals etc.

user = "smartlockAGH@gmail.com"
password = "satokG12"

try:
    f = open("logs/mailing.log", 'r')     #open list of addresses
    mail_list = (f.read().splitlines())                                  #load addresses
    f.close()
except:
    print("Problem with loading addresses mail")

def sendmail(code):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sent_from = "SMARTLOCK"
    code = str(code)                          #current passcode
    now = datetime.datetime.today()
    now_str = now.strftime("%d/%m/%Y")         #get current date for subject
    subject = "SmartLock Passcode " + now_str

    body = "Czesc,\nAktualny kod to SmartLocka to "+code+".\n\nNie przeyslaj tego " \
             "maila dalej, ani nie dziel sie kodem z osobami z poza kola\n\nPozdrawiamy,\nZespol SmartLock"

    email_text = """\
From: %s    
    
Subject: %s

%s""" % (sent_from, subject, body)

    try:
        sent_to = mail_list
        print(mail_list)
        print(body)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)              #choosing server and port for communication
        smtp_server.ehlo()
        smtp_server.login(user,password)                                   #logging to server
        smtp_server.sendmail(sent_from, sent_to, email_text.encode("utf8"))    #sending mail
        smtp_server.close()                                                #closing connection
        print("Email sent successfully!"+body)
    except:
        print("Problem wtih sending mail")

