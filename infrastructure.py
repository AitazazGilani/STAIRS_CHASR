import boto3

# AWS credentials and region
aws_access_key = 'YOUR_ACCESS_KEY'
aws_secret_key = 'YOUR_SECRET_KEY'
aws_region = 'us-east-1'  # Replace with your desired region

# EC2 instance parameters
ami_id = 'YOUR_AMI_ID'  # Replace with your AMI ID
instance_type = 't2.micro'  # Replace with your desired instance type
key_pair_name = 'YOUR_KEY_PAIR_NAME'  # Replace with your key pair name
security_group_name = 'YOUR_SECURITY_GROUP_NAME'  # Replace with your security group name

# User data (startup script)
user_data = '''
#!/bin/bash
# Add your startup commands here
'''

# Create an EC2 client
ec2 = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Create a security group
response = ec2.create_security_group(
    Description='My Security Group',
    GroupName=security_group_name,
    VpcId='YOUR_VPC_ID'  # Replace with your VPC ID
)

# Add inbound rules to the security group
ec2.authorize_security_group_ingress(
    GroupId=response['GroupId'],
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 8080,
            'ToPort': 8080,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 5432,
            'ToPort': 5432,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

# Launch the EC2 instance with the specified configuration
response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=key_pair_name,
    SecurityGroups=[security_group_name],
    UserData=user_data,
    MinCount=1,
    MaxCount=1
)

print(f'Launched EC2 instance with Instance ID: {response["Instances"][0]["InstanceId"]}')
