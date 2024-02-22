import boto3
import csv
from pprint import pprint
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def lambda_handler(event, context):
    # Start the Ec2
    ec2_client = boto3.client('ec2')
    waiter = ec2_client.get_waiter('instance_running')
    instance_ids = ['i-0c094300ef6d27462', 'i-022ba6928b04714d5']
    response = ec2_client.start_instances(InstanceIds=instance_ids)
    waiter.wait(InstanceIds=instance_ids)
    print("instances are up and running fine")

    # To create inventory files
    ec2_con_re = boto3.resource(service_name="ec2", region_name="us-east-1")
    cnt = 1
    csv_path = '/tmp/inventory_info.csv'
    with open(csv_path, "w", newline='') as csv_ob:
        csv_w = csv.writer(csv_ob)
        csv_w.writerow(["S_NO", 'Instance_Name', "Instance_Id", 'Instance_Type', 'LaunchTime', 'Private_Ip',
                        'Public_IP', 'Security_Group', 'Status', 'VPC_ID'])

        for each in ec2_con_re.instances.all():
            for name in each.tags:
                Name = name['Value']
            print(Name, each.instance_id, each.instance_type, each.launch_time.strftime("%Y-%m-%d"),
                  each.private_ip_address, each.public_ip_address,
                  each.security_groups, each.state['Name'], each.vpc_id
                  )
            csv_w.writerow([cnt, Name, each.instance_id, each.instance_type,
                            each.launch_time.strftime("%Y-%m-%d"),
                            each.private_ip_address, each.public_ip_address,
                            each.security_groups, each.state['Name'], each.vpc_id]
                           )
            cnt += 1

    # # Uploading file to s3
    # s3 = boto3.client('s3')
    # bucket_name = 'my-puch-te'
    # s3.upload_file(csv_path, bucket_name, 'inventory_info.csv')

    # # Clean up: Optionally delete the file after uploading
    # os.remove(csv_path)

    # triggering mail

    msg = MIMEMultipart()
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    msg["Subject"] = f"START INSTANCE SUCCEEDED ON {today_date}"
    # msg["From"] = "zthambz@gmail.com"
    # msg["To"] = "zthambz@gmail.com"

    body = MIMEText(
        f"Hi Team\n\nThe following instance are up and running fine. Kindly check with attached csv to get the public ip.\nThe Instances are {instance_ids}")
    msg.attach(body)

    filename = "/tmp/inventory_info.csv"

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
        RawMessage={"Data": msg.as_string()}

    )

    print(response)