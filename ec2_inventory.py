import boto3
import csv
from pprint import pprint
ec2_con_re = boto3.resource(service_name="ec2", region_name="us-east-1")
cnt = 1
csv_ob = open("inventory_info.csv", "w", newline='')
csv_w = csv.writer(csv_ob)
csv_w.writerow(["S_NO", "Instance_Id", 'Instance_Type', 'LaunchTime', 'Private_Ip',
                'Public_IP', 'Security_Group', 'Status', 'Tags', 'VPC_ID'])
for each in ec2_con_re.instances.all():
    # pprint(dir(each))
    print(each.instance_id, each.instance_type, each.launch_time.strftime("%Y-%m-%d"),
          each.private_ip_address, each.public_ip_address,
          each.security_groups, each.state['Name'], each.tags, each.vpc_id
          )
    # print(cnt,each,each.instance_id,each.instance_type,each.architecture,each.launch_time.strftime("%Y-%m-%d"),each.private_ip_address)
    csv_w.writerow([cnt, each.instance_id,each.instance_type,
                    each.launch_time.strftime("%Y-%m-%d"),
                    each.private_ip_address, each.public_ip_address,
                    each.security_groups, each.state['Name'], each.tags, each.vpc_id]
                   )
    cnt += 1
csv_ob.close()
