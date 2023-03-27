import smtplib, ssl
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import requests
import pandas as pd


current_date = '2023-03-27'
# The API endpoint
url = f"http://issue.c1.biz/data.php?current_date={current_date}"

# A GET request to the API
response = requests.get(url)

# Print the response
response_json = response.json()

data = pd.DataFrame(response_json)
data = data.reset_index()
data['index'] = data['index']+1
del data['id']

data.rename({"index": "Sr.No",
             "issue" : "Issue/Problem",
            "issue_solution": "Resolution",
            "issue_for_user": "Users",
            "department": "Department",
            "issue_engineer": "Engineer",
            "issue_status": "Status",
            "issue_date": "Date"}, axis=1, inplace=True)

data['Time'] = data['issue_time_from']+' - '+data['issue_time_to']
del data['issue_time_from']
del data['issue_time_to']


current_date_str = current_date.replace('-','_')
data.to_excel("Issue-Report_"+current_date_str+".xlsx", index=False)

#=====================================
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

send_mail(sender,destination, "Test", "Hii", ["Issue-Report_"+current_date_str+".xlsx"],smtp_server, 587, USERNAME, PASSWORD)

# message = """\
# Subject: GitHub Email Report
# This is your daily email report.
# """

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(USERNAME,PASSWORD)
#     server.sendmail(sender,destination,message)


