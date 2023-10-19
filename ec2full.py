import boto3
import pandas as pd


# Initialize AWS client
ec2_client = boto3.client('ec2')

# Function to get all instances in the account
def get_all_instances():
    instances = ec2_client.describe_instances()
    return [instance for reservation in instances['Reservations'] for instance in reservation['Instances']]

# Get all instances
instances = get_all_instances()

# List to store instance details
instance_details = []

# Fetch instance details
for instance in instances:
    instance_id = instance['InstanceId']
    instance_name = [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']
    instance_name = instance_name[0] if instance_name else '-'
    
    instance_tags = instance.get('Tags', [])
    tags_dict = {tag['Key']: tag['Value'] for tag in instance_tags}
    private_ip = instance.get('PrivateIpAddress', '-')
    public_ip = instance.get('PublicIpAddress', '-')
    availability_zone = instance.get('Placement', {}).get('AvailabilityZone', '-')
    instance_type = instance.get('InstanceType', '-')
    
    instance_details.append({
        'Instance ID': instance_id,
        'Instance Name': instance_name,
        'Tags': tags_dict,
        'Private IP': private_ip,
        'Public IP': public_ip,
        'Availability Zone': availability_zone,
        'Instance Type': instance_type,
    })

# Create a DataFrame from the instance details
df = pd.DataFrame(instance_details)

# Save the DataFrame to an Excel file
df.to_excel('aws_instance_details_with_tags.xlsx', index=False)


