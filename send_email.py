import smtplib, ssl
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')

sender =     'ankit.velani@gmail.com'
destination = ['ankit.velani@gmail.com', 'velaniankits@gmail.com']


message = """\
Subject: GitHub Email Report
This is your daily email report.
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME,PASSWORD)
    server.sendmail(sender,destination,message)
