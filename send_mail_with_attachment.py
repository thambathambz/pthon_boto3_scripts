import boto3

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def lambda_handler(event, context):
    msg = MIMEMultipart()

    msg["Subject"] = "This is python with boto3 course"
    msg["From"] = "zthambz@gmail.com"
    msg["To"] = "zthambz@gmail.com"

    body = MIMEText("Aws with Python & Boto3, Thanks for buying the course")
    msg.attach(body)


    filename = "inventory_info.csv"

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)

    msg.attach(part)


    ses_client = boto3.client('ses')
    response = ses_client.send_raw_email(
        Source="zthambz@gmail.com",
        Destinations=["zthambz@gmail.com"],
        RawMessage={"Data":msg.as_string()}

    )

    print(response)



send_email_attachment()
