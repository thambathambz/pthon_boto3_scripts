import json
import boto3
from pprint import pprint

ec2_client = boto3.client('ec2')
waiter = ec2_client.get_waiter('instance_running')
instance_ids = ['###', '###']
response = ec2_client.start_instances(InstanceIds=instance_ids)
waiter.wait(InstanceIds=instance_ids)
print("instances are up and running fine")

