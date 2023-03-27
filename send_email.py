import smtplib, ssl
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')

sender =     'ankit.velani@gmail.com'
destination = ['ankit.velani@gmail.com', 'velaniankits@gmail.com']


def send_mail(send_from, send_to, subject, message, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

send_mail(sender,destination, "Test", "Hii", ['send_email.py'],smtp_server, 587, USERNAME, PASSWORD)

# message = """\
# Subject: GitHub Email Report
# This is your daily email report.
# """

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(USERNAME,PASSWORD)
#     server.sendmail(sender,destination,message)


