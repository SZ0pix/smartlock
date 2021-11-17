# Import smtplib for the actual sending function
import smtplib
import datetime

user = "smartlockAGH@gmail.com"
password = "satokG12"
#code=1234

try:
    f = open("C:/Users/mjszo/OneDrive/Pulpit/mailing.log", 'r')
    list = (f.read().splitlines())
    f.close()
except:
    print("problem")


def sendmail(kod):
    sent_from = "SMARTLOCK"
    kod = str(kod)
    now = datetime.datetime.today()
    nowStr = now.strftime("%d/%m/%Y")
    subject = "SmartLock Passcode " + nowStr

    body = "Czesc,\nAktualny kod to SmartLocka to "+kod+".\n\nNie przeyslaj tego " \
             "maila dalej, ani nie dziel sie kodem z osobami z poza kola\n\nPozdrawiamy,\nZespol SmartLock"

    email_text = """\
From: %s    
    
Subject: %s

%s""" % (sent_from, subject, body)


    try:
        sent_to = list
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(user,password)
        smtp_server.sendmail(sent_from, sent_to, email_text.encode("utf8"))
        smtp_server.close()
        print ("Email sent successfully!"+body)
    except Exception as ex:
        print ("Something went wrong….",ex)
