# To get the un used volumes
import boto3
from pprint import pprint

ec2_con = boto3.client('ec2')
response = ec2_con.describe_volumes()

for each_item in response['Volumes']:
    try:
        print(f"{each_item['VolumeId']} ,{each_item['State']}, {each_item['Tags']}")
    except KeyError:
        each_item['Tags'] = None
        print(f"{each_item['VolumeId']} ,{each_item['State']}, {each_item['Tags']}")

print("################################################################################")
res = ec2_con.describe_volumes()

unused_volumes = []
for each_item in res['Volumes']:
    if each_item['State'] == 'available' and "Tags" not in each_item:
        unused_volumes.append(each_item['VolumeId'])

print(f"Below volumes are Available state and Tags also not set \n{unused_volumes}")


if not unused_volumes:
    print("There is no un used volumes")
else:
    delete_volumes = input(f"Do you want me to delete volume which is not in use and not in Tags? 'yes' or 'no': ").lower()
    if delete_volumes == "yes":
        for volume in unused_volumes:
            ec2_con.delete_volume(VolumeId=volume)
        print("Volumes are deleted successfully")
    else:
        print("We are not deleting it. Thank you!!!")
