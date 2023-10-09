import boto3

# AWS credentials and region
aws_access_key = 'YOUR_ACCESS_KEY'
aws_secret_key = 'YOUR_SECRET_KEY'
aws_region = 'us-east-1'  # Replace with your desired region

# User data (startup script)
with open('start.sh', 'r') as start_script_file:
    user_data = start_script_file.read()

# Create an EC2 client
ec2 = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Get the default VPC ID
response = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
default_vpc_id = response['Vpcs'][0]['VpcId']

# Create an EBS volume
response = ec2.create_volume(
    AvailabilityZone=aws_region + 'a',  # Replace 'a' with the desired availability zone
    Size=30,
    VolumeType='gp2'
)

ebs_volume_id = response['VolumeId']

# Wait for the EBS volume to be available
ec2.get_waiter('volume_available').wait(VolumeIds=[ebs_volume_id])

# Launch the EC2 instance with the specified configuration
response = ec2.run_instances(
    ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2 AMI ID
    InstanceType='t2.micro',
    KeyName='YOUR_KEY_PAIR_NAME',  # Replace with your key pair name
    SecurityGroups=['YOUR_SECURITY_GROUP_NAME'],  # Replace with your security group name
    UserData=user_data,
    MinCount=1,
    MaxCount=1,
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeId': ebs_volume_id,
                'DeleteOnTermination': True
            },
        },
    ],
    SubnetId=default_vpc_id  # Use the default VPC
)

instance_id = response['Instances'][0]['InstanceId']

print(f'Launched EC2 instance with Instance ID: {instance_id}')
