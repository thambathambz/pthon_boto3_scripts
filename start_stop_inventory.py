import boto3
import csv
from pprint import pprint
import os


def lambda_handler(event, context):
    # Start the Ec2
    ec2_client = boto3.client('ec2')
    waiter = ec2_client.get_waiter('instance_running')
    instance_ids = ['###', '###']
    response = ec2_client.start_instances(InstanceIds=instance_ids)
    waiter.wait(InstanceIds=instance_ids)
    print("instances are up and running fine")

    # To create inventory files
    ec2_con_re = boto3.resource(service_name="ec2", region_name="us-east-1")
    cnt = 1
    csv_path = '/tmp/inventory_info.csv'
    with open(csv_path, "w", newline='') as csv_ob:
        csv_w = csv.writer(csv_ob)
        csv_w.writerow(["S_NO", "Instance_Id", 'Instance_Type', 'LaunchTime', 'Private_Ip',
                        'Public_IP', 'Security_Group', 'Status', 'Tags', 'VPC_ID'])

        for each in ec2_con_re.instances.all():
            print(each.instance_id, each.instance_type, each.launch_time.strftime("%Y-%m-%d"),
                  each.private_ip_address, each.public_ip_address,
                  each.security_groups, each.state['Name'], each.tags, each.vpc_id
                  )
            csv_w.writerow([cnt, each.instance_id, each.instance_type,
                            each.launch_time.strftime("%Y-%m-%d"),
                            each.private_ip_address, each.public_ip_address,
                            each.security_groups, each.state['Name'], each.tags, each.vpc_id]
                           )
            cnt += 1

    # Uploading file to s3
    s3 = boto3.client('s3')
    bucket_name = 'my-puch-te'
    s3.upload_file(csv_path, bucket_name, 'inventory_info.csv')

    # Clean up: Optionally delete the file after uploading
    os.remove(csv_path)