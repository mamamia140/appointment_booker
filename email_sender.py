from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import ssl
import os

SMTP_SERVER_ADDRESS = "smtp-mail.outlook.com"
SMTP_SERVER_PORT = 587
load_dotenv()

class MailServer(smtplib.SMTP):

    context = None
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_EMAIL_PASSWORD")
    receiver = os.getenv("RECEIVER_EMAIL")
    message = EmailMessage()
    

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        super().__init__(host=SMTP_SERVER_ADDRESS, port= SMTP_SERVER_PORT)
        self.context = ssl.create_default_context()
        self.starttls(context=self.context)
        self.message['Content-Type'] = 'text/plain'
        self.message['Subject'] = 'There is an available appointment slot'
        self.message['From'] = self.sender
        self.message['To'] = self.receiver

        print(self.message.keys())
        print(self.message.values())

    def authenticate(self):
        self.login(self.sender,self.password)
  
    def send_mail(self):
        self.send_message(self.message)



