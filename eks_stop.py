from pprint import pprint
import boto3

eks_console = boto3.client('eks')
response = (eks_console.update_nodegroup_config
            (clusterName="tst",
             nodegroupName='test',
             scalingConfig={
                 'minSize': 0,
                 'maxSize': 1,
                 'desiredSize': 0
             },
             ))
pprint(response)
