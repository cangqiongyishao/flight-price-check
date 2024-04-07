import smtplib,ssl
import os

class NotificationManager:

    def send_email(self,message):
        host='smtp.gmail.com'
        port=465
        username=os.getenv('GMAIL')
        password=os.getenv('PASSWORD')

        receiver='cangqiongyishao@yahoo.com'
        context=ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)