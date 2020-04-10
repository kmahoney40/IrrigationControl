import logging
import datetime
import smtplib
import socket
import string


class mail:
    def __init__(self):
        self.today = datetime.date.today()
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_obj.starttls()
        self.smtp_obj.login('k.mahohney.40@gmail.com','mQTwsUzys2panGZ')
        self.sender = 'k.mahohney.40@gamil.com'
        self.subject = "Daily Update"
        self.body = ""
        self.receivers = ['kmahoney40@hotmail.com']
        self.message = """
        From k.mahohney.40@gmail.com
        To kmahoney40@hotmail.com
        Subject: {}

        {}
        Current IP: {}
        Time: {}
        """
    #def __init__

    def send_mail(self, sub=None, bod=None):
        dtnow = str(datetime.datetime.now())
    
        if sub != None:
            self.subject = sub
        if bod != None:
            self.body = bod
        self.host_ip = socket.gethostbyname(self.host_name)
        ipAsList = string.split(self.host_ip, ".")
        self.host_ip = "x.x." + ipAsList[2] + "." + ipAsList[3]
        self.message = self.message.format(self.subject, self.body, self.host_ip, dtnow)
        self.smtp_obj.sendmail(self.sender, self.receivers, self.message)
        self.smtp_obj.quit() 
        
     # def send_mail()
# class mail
