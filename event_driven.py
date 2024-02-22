import boto3

from pprint import pprint
ec2_con = boto3.client("ec2")
response = ec2_con.describe_instances()
print("The available instances are")
for each_item in response['Reservations']:
    for each_instance in each_item['Instances']:
        # print(each_instance)
        print(each_instance.get('InstanceId'))

print('''
        Choose the Options\n
        1. Start Instances\n
        2. Stop Instances\n
        3. Terminate Instances\n
        4. Exit
        ''')
is_continue = True
while is_continue:
    option = int(input("Choose your options: "))
    if option == 1:
        instance_id = input("Which instance you want to start? ")
        ec2_con.start_instances(InstanceIds=[instance_id])
        print("Starting Instance...")
    elif option == 2:
        instance_id = input("Which instance you want to stop? ")
        ec2_con.stop_instances(InstanceIds=[instance_id])
        print("Stopping Instance....")
    elif option == 3:
        instance_id = input("Which instance you want to stop? ")
        ec2_con.terminate_instances(InstanceIds=[instance_id])
        print("Terminating instances...")
    elif option == 4:
        print("Exit")
        print("Thank you! Come Again")
        is_continue = False
    else:
        print("Invalid option. Choose correct option from 1 to 4")

