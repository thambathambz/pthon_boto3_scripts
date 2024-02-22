import boto3
from pprint import pprint

ec2_con_re = boto3.resource('ec2')

for each in ec2_con_re.instances.all():
    for name in each.tags:
        Name = name['Value']
    print(each.instance_id, each.instance_type, each.launch_time.strftime("%Y-%m-%d"),
          each.private_ip_address, each.public_ip_address,
          each.security_groups, each.state['Name'], Name, each.vpc_id
          )
