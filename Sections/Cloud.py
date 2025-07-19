import streamlit as st
import boto3
import json
import pandas as pd
from datetime import datetime
import os

def log_command(command):
    """Log command to file"""
    with open("command_log.txt", "a") as f:
        f.write(f"{datetime.now()}: {command}\n")

def get_aws_client(service_name, region_name='us-east-1'):
    """Get AWS client with credentials"""
    try:
        # Try to get credentials from session state or environment
        aws_access_key = st.session_state.get('aws_access_key') or os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = st.session_state.get('aws_secret_key') or os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if aws_access_key and aws_secret_key:
            return boto3.client(
                service_name,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region_name
            )
        else:
            # Try to use default credentials
            return boto3.client(service_name, region_name=region_name)
    except Exception as e:
        st.error(f"Error creating AWS client: {e}")
        return None

def cloud_section(sub_choice=None):
    st.markdown('<h1 class="section-header">☁️ AWS Cloud Management</h1>', unsafe_allow_html=True)
    
    # AWS Configuration
    st.subheader("🔧 AWS Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        aws_access_key = st.text_input("AWS Access Key ID:", type="password")
        if aws_access_key:
            st.session_state.aws_access_key = aws_access_key
    
    with col2:
        aws_secret_key = st.text_input("AWS Secret Access Key:", type="password")
        if aws_secret_key:
            st.session_state.aws_secret_key = aws_secret_key
    
    region = st.selectbox("AWS Region:", [
        'us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1', 'ap-northeast-1'
    ])
    
    if st.button("🔗 Test AWS Connection"):
        ec2_client = get_aws_client('ec2', region)
        if ec2_client:
            try:
                response = ec2_client.describe_regions()
                st.success("✅ AWS connection successful!")
                st.session_state.aws_region = region
            except Exception as e:
                st.error(f"❌ AWS connection failed: {e}")
        else:
            st.error("❌ Failed to create AWS client")
    
    if sub_choice == "🚀 AWS EC2":
        ec2_section(region)
    elif sub_choice == "📦 S3 Buckets":
        s3_section(region)
    elif sub_choice == "🔐 IAM Roles":
        iam_section(region)
    elif sub_choice == "💾 EBS Volumes":
        ebs_section(region)
    else:
        st.info("Please select an AWS service from the sidebar.")

def ec2_section(region):
    st.subheader("🚀 EC2 Instance Management")
    
    ec2_client = get_aws_client('ec2', region)
    if not ec2_client:
        st.error("❌ Failed to create EC2 client")
        return
    
    # Create tabs for different EC2 operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Instances", "🚀 Launch Instance", "🔧 Instance Operations", "📊 Monitoring"
    ])
    
    with tab1:
        st.subheader("📋 EC2 Instances")
        
        if st.button("🔄 Refresh Instances"):
            try:
                response = ec2_client.describe_instances()
                instances = []
                
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        instances.append({
                            'Instance ID': instance['InstanceId'],
                            'Instance Type': instance['InstanceType'],
                            'State': instance['State']['Name'],
                            'Launch Time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                            'Public IP': instance.get('PublicIpAddress', 'N/A'),
                            'Private IP': instance.get('PrivateIpAddress', 'N/A'),
                            'Platform': instance.get('Platform', 'linux')
                        })
                
                if instances:
                    df = pd.DataFrame(instances)
                    st.dataframe(df)
                    st.session_state.ec2_instances = instances
                    log_command(f"AWS EC2: Listed {len(instances)} instances")
                else:
                    st.info("No EC2 instances found")
                    
            except Exception as e:
                st.error(f"Error listing instances: {e}")
        
        # Display instances if available
        if 'ec2_instances' in st.session_state:
            st.subheader("📋 Current Instances")
            df = pd.DataFrame(st.session_state.ec2_instances)
            st.dataframe(df)
    
    with tab2:
        st.subheader("🚀 Launch New Instance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Instance configuration
            instance_name = st.text_input("Instance Name:", value="my-instance")
            instance_type = st.selectbox("Instance Type:", [
                't2.micro', 't2.small', 't2.medium', 't3.micro', 't3.small', 't3.medium'
            ])
            
            # AMI selection
            ami_id = st.text_input("AMI ID:", value="ami-0c55b159cbfafe1f0")  # Amazon Linux 2
            
            # Key pair
            key_name = st.text_input("Key Pair Name:", value="my-key-pair")
        
        with col2:
            # Security group
            security_group = st.text_input("Security Group ID:", value="sg-0123456789abcdef0")
            
            # Subnet
            subnet_id = st.text_input("Subnet ID:", value="subnet-0123456789abcdef0")
            
            # Storage
            volume_size = st.number_input("Volume Size (GB):", min_value=8, max_value=100, value=20)
        
        if st.button("🚀 Launch Instance"):
            try:
                response = ec2_client.run_instances(
                    ImageId=ami_id,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=instance_type,
                    KeyName=key_name,
                    SecurityGroupIds=[security_group],
                    SubnetId=subnet_id,
                    BlockDeviceMappings=[
                        {
                            'DeviceName': '/dev/xvda',
                            'Ebs': {
                                'VolumeSize': volume_size,
                                'VolumeType': 'gp2',
                                'DeleteOnTermination': True
                            }
                        }
                    ],
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': instance_name
                                }
                            ]
                        }
                    ]
                )
                
                instance_id = response['Instances'][0]['InstanceId']
                st.success(f"✅ Instance {instance_id} launched successfully!")
                log_command(f"AWS EC2: Launched instance {instance_id}")
                
            except Exception as e:
                st.error(f"Error launching instance: {e}")
    
    with tab3:
        st.subheader("🔧 Instance Operations")
        
        if 'ec2_instances' in st.session_state and st.session_state.ec2_instances:
            instance_id = st.selectbox("Select Instance:", 
                                     [inst['Instance ID'] for inst in st.session_state.ec2_instances])
            
            if instance_id:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("▶️ Start Instance"):
                        try:
                            ec2_client.start_instances(InstanceIds=[instance_id])
                            st.success(f"Instance {instance_id} starting...")
                            log_command(f"AWS EC2: Started instance {instance_id}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col2:
                    if st.button("⏸️ Stop Instance"):
                        try:
                            ec2_client.stop_instances(InstanceIds=[instance_id])
                            st.success(f"Instance {instance_id} stopping...")
                            log_command(f"AWS EC2: Stopped instance {instance_id}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col3:
                    if st.button("🔄 Reboot Instance"):
                        try:
                            ec2_client.reboot_instances(InstanceIds=[instance_id])
                            st.success(f"Instance {instance_id} rebooting...")
                            log_command(f"AWS EC2: Rebooted instance {instance_id}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col4:
                    if st.button("🗑️ Terminate Instance"):
                        if st.checkbox("I understand this will permanently delete the instance"):
                            try:
                                ec2_client.terminate_instances(InstanceIds=[instance_id])
                                st.success(f"Instance {instance_id} terminating...")
                                log_command(f"AWS EC2: Terminated instance {instance_id}")
                            except Exception as e:
                                st.error(f"Error: {e}")
        else:
            st.info("No instances available. Please refresh instances first.")
    
    with tab4:
        st.subheader("📊 EC2 Monitoring")
        
        if st.button("📊 Get Instance Status"):
            try:
                response = ec2_client.describe_instance_status()
                if response['InstanceStatuses']:
                    status_data = []
                    for status in response['InstanceStatuses']:
                        status_data.append({
                            'Instance ID': status['InstanceId'],
                            'State': status['InstanceState']['Name'],
                            'Status Check': status['InstanceStatus']['Status'],
                            'System Check': status['SystemStatus']['Status']
                        })
                    
                    df = pd.DataFrame(status_data)
                    st.dataframe(df)
                else:
                    st.info("No instance status information available")
                    
            except Exception as e:
                st.error(f"Error getting instance status: {e}")

def s3_section(region):
    st.subheader("📦 S3 Bucket Management")
    
    s3_client = get_aws_client('s3', region)
    if not s3_client:
        st.error("❌ Failed to create S3 client")
        return
    
    # Create tabs for different S3 operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Buckets", "📁 Objects", "📤 Upload", "🔧 Bucket Operations"
    ])
    
    with tab1:
        st.subheader("📋 S3 Buckets")
        
        if st.button("🔄 List Buckets"):
            try:
                response = s3_client.list_buckets()
                buckets = []
                
                for bucket in response['Buckets']:
                    # Get bucket location
                    try:
                        location = s3_client.get_bucket_location(Bucket=bucket['Name'])
                        region_name = location['LocationConstraint'] or 'us-east-1'
                    except:
                        region_name = 'N/A'
                    
                    buckets.append({
                        'Bucket Name': bucket['Name'],
                        'Creation Date': bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Region': region_name
                    })
                
                if buckets:
                    df = pd.DataFrame(buckets)
                    st.dataframe(df)
                    st.session_state.s3_buckets = buckets
                    log_command(f"AWS S3: Listed {len(buckets)} buckets")
                else:
                    st.info("No S3 buckets found")
                    
            except Exception as e:
                st.error(f"Error listing buckets: {e}")
        
        # Create new bucket
        st.subheader("🆕 Create New Bucket")
        new_bucket_name = st.text_input("Bucket Name:")
        
        if st.button("🆕 Create Bucket"):
            if new_bucket_name:
                try:
                    s3_client.create_bucket(Bucket=new_bucket_name)
                    st.success(f"✅ Bucket {new_bucket_name} created successfully!")
                    log_command(f"AWS S3: Created bucket {new_bucket_name}")
                except Exception as e:
                    st.error(f"Error creating bucket: {e}")
            else:
                st.warning("Please provide a bucket name")
    
    with tab2:
        st.subheader("📁 S3 Objects")
        
        if 's3_buckets' in st.session_state and st.session_state.s3_buckets:
            bucket_name = st.selectbox("Select Bucket:", 
                                     [bucket['Bucket Name'] for bucket in st.session_state.s3_buckets])
            
            if bucket_name and st.button("📁 List Objects"):
                try:
                    response = s3_client.list_objects_v2(Bucket=bucket_name)
                    
                    if 'Contents' in response:
                        objects = []
                        for obj in response['Contents']:
                            objects.append({
                                'Key': obj['Key'],
                                'Size (Bytes)': obj['Size'],
                                'Last Modified': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                                'Storage Class': obj['StorageClass']
                            })
                        
                        df = pd.DataFrame(objects)
                        st.dataframe(df)
                        st.session_state.s3_objects = objects
                    else:
                        st.info(f"No objects found in bucket {bucket_name}")
                        
                except Exception as e:
                    st.error(f"Error listing objects: {e}")
        else:
            st.info("No buckets available. Please list buckets first.")
    
    with tab3:
        st.subheader("📤 Upload File")
        
        if 's3_buckets' in st.session_state and st.session_state.s3_buckets:
            bucket_name = st.selectbox("Select Bucket for Upload:", 
                                     [bucket['Bucket Name'] for bucket in st.session_state.s3_buckets])
            
            uploaded_file = st.file_uploader("Choose a file to upload", type=['txt', 'csv', 'json', 'py', 'jpg', 'png'])
            
            if uploaded_file and bucket_name:
                object_key = st.text_input("Object Key (filename in S3):", value=uploaded_file.name)
                
                if st.button("📤 Upload"):
                    try:
                        s3_client.upload_fileobj(uploaded_file, bucket_name, object_key)
                        st.success(f"✅ File uploaded successfully to s3://{bucket_name}/{object_key}")
                        log_command(f"AWS S3: Uploaded {object_key} to {bucket_name}")
                    except Exception as e:
                        st.error(f"Error uploading file: {e}")
        else:
            st.info("No buckets available. Please list buckets first.")
    
    with tab4:
        st.subheader("🔧 Bucket Operations")
        
        if 's3_buckets' in st.session_state and st.session_state.s3_buckets:
            bucket_name = st.selectbox("Select Bucket for Operations:", 
                                     [bucket['Bucket Name'] for bucket in st.session_state.s3_buckets])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Delete Bucket"):
                    if st.checkbox("I understand this will permanently delete the bucket and all contents"):
                        try:
                            # Delete all objects first
                            response = s3_client.list_objects_v2(Bucket=bucket_name)
                            if 'Contents' in response:
                                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                                s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
                            
                            s3_client.delete_bucket(Bucket=bucket_name)
                            st.success(f"✅ Bucket {bucket_name} deleted successfully!")
                            log_command(f"AWS S3: Deleted bucket {bucket_name}")
                        except Exception as e:
                            st.error(f"Error deleting bucket: {e}")
            
            with col2:
                if st.button("📊 Get Bucket Info"):
                    try:
                        response = s3_client.get_bucket_versioning(Bucket=bucket_name)
                        st.write("Bucket Versioning:", response.get('Status', 'Not enabled'))
                        
                        # Get bucket size
                        response = s3_client.list_objects_v2(Bucket=bucket_name)
                        total_size = sum(obj['Size'] for obj in response.get('Contents', []))
                        st.write(f"Total Size: {total_size} bytes")
                        
                    except Exception as e:
                        st.error(f"Error getting bucket info: {e}")
        else:
            st.info("No buckets available. Please list buckets first.")

def iam_section(region):
    st.subheader("🔐 IAM Management")
    
    iam_client = get_aws_client('iam', region)
    if not iam_client:
        st.error("❌ Failed to create IAM client")
        return
    
    # Create tabs for different IAM operations
    tab1, tab2, tab3 = st.tabs([
        "👥 Users", "🔑 Access Keys", "📋 Policies"
    ])
    
    with tab1:
        st.subheader("👥 IAM Users")
        
        if st.button("🔄 List Users"):
            try:
                response = iam_client.list_users()
                users = []
                
                for user in response['Users']:
                    users.append({
                        'User Name': user['UserName'],
                        'User ID': user['UserId'],
                        'ARN': user['Arn'],
                        'Create Date': user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                if users:
                    df = pd.DataFrame(users)
                    st.dataframe(df)
                    st.session_state.iam_users = users
                    log_command(f"AWS IAM: Listed {len(users)} users")
                else:
                    st.info("No IAM users found")
                    
            except Exception as e:
                st.error(f"Error listing users: {e}")
        
        # Create new user
        st.subheader("🆕 Create New User")
        new_user_name = st.text_input("User Name:")
        
        if st.button("🆕 Create User"):
            if new_user_name:
                try:
                    iam_client.create_user(UserName=new_user_name)
                    st.success(f"✅ User {new_user_name} created successfully!")
                    log_command(f"AWS IAM: Created user {new_user_name}")
                except Exception as e:
                    st.error(f"Error creating user: {e}")
            else:
                st.warning("Please provide a user name")
    
    with tab2:
        st.subheader("🔑 Access Keys")
        
        if 'iam_users' in st.session_state and st.session_state.iam_users:
            user_name = st.selectbox("Select User:", 
                                   [user['User Name'] for user in st.session_state.iam_users])
            
            if user_name and st.button("🔑 List Access Keys"):
                try:
                    response = iam_client.list_access_keys(UserName=user_name)
                    
                    if response['AccessKeyMetadata']:
                        keys = []
                        for key in response['AccessKeyMetadata']:
                            keys.append({
                                'Access Key ID': key['AccessKeyId'],
                                'Status': key['Status'],
                                'Create Date': key['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
                            })
                        
                        df = pd.DataFrame(keys)
                        st.dataframe(df)
                    else:
                        st.info(f"No access keys found for user {user_name}")
                        
                except Exception as e:
                    st.error(f"Error listing access keys: {e}")
        else:
            st.info("No users available. Please list users first.")
    
    with tab3:
        st.subheader("📋 IAM Policies")
        
        if st.button("📋 List Policies"):
            try:
                response = iam_client.list_policies(Scope='Local')
                policies = []
                
                for policy in response['Policies']:
                    policies.append({
                        'Policy Name': policy['PolicyName'],
                        'Policy ID': policy['PolicyId'],
                        'ARN': policy['Arn'],
                        'Create Date': policy['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                if policies:
                    df = pd.DataFrame(policies)
                    st.dataframe(df)
                    log_command(f"AWS IAM: Listed {len(policies)} policies")
                else:
                    st.info("No IAM policies found")
                    
            except Exception as e:
                st.error(f"Error listing policies: {e}")

def ebs_section(region):
    st.subheader("💾 EBS Volume Management")
    
    ec2_client = get_aws_client('ec2', region)
    if not ec2_client:
        st.error("❌ Failed to create EC2 client")
        return
    
    # Create tabs for different EBS operations
    tab1, tab2, tab3 = st.tabs([
        "📋 Volumes", "🔧 Volume Operations", "📸 Snapshots"
    ])
    
    with tab1:
        st.subheader("📋 EBS Volumes")
        
        if st.button("🔄 List Volumes"):
            try:
                response = ec2_client.describe_volumes()
                volumes = []
                
                for volume in response['Volumes']:
                    attachments = []
                    for attachment in volume['Attachments']:
                        attachments.append(attachment['InstanceId'])
                    
                    volumes.append({
                        'Volume ID': volume['VolumeId'],
                        'Size (GB)': volume['Size'],
                        'Volume Type': volume['VolumeType'],
                        'State': volume['State'],
                        'Availability Zone': volume['AvailabilityZone'],
                        'Attached To': ', '.join(attachments) if attachments else 'Not attached'
                    })
                
                if volumes:
                    df = pd.DataFrame(volumes)
                    st.dataframe(df)
                    st.session_state.ebs_volumes = volumes
                    log_command(f"AWS EBS: Listed {len(volumes)} volumes")
                else:
                    st.info("No EBS volumes found")
                    
            except Exception as e:
                st.error(f"Error listing volumes: {e}")
        
        # Create new volume
        st.subheader("🆕 Create New Volume")
        
        col1, col2 = st.columns(2)
        with col1:
            volume_size = st.number_input("Size (GB):", min_value=1, max_value=16384, value=20)
            volume_type = st.selectbox("Volume Type:", ['gp2', 'gp3', 'io1', 'io2', 'st1', 'sc1'])
        
        with col2:
            availability_zone = st.text_input("Availability Zone:", value="us-east-1a")
            encrypted = st.checkbox("Encrypted")
        
        if st.button("🆕 Create Volume"):
            try:
                kwargs = {
                    'Size': volume_size,
                    'AvailabilityZone': availability_zone,
                    'VolumeType': volume_type,
                    'Encrypted': encrypted
                }
                
                response = ec2_client.create_volume(**kwargs)
                volume_id = response['VolumeId']
                st.success(f"✅ Volume {volume_id} created successfully!")
                log_command(f"AWS EBS: Created volume {volume_id}")
                
            except Exception as e:
                st.error(f"Error creating volume: {e}")
    
    with tab2:
        st.subheader("🔧 Volume Operations")
        
        if 'ebs_volumes' in st.session_state and st.session_state.ebs_volumes:
            volume_id = st.selectbox("Select Volume:", 
                                   [vol['Volume ID'] for vol in st.session_state.ebs_volumes])
            
            if volume_id:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🗑️ Delete Volume"):
                        if st.checkbox("I understand this will permanently delete the volume"):
                            try:
                                ec2_client.delete_volume(VolumeId=volume_id)
                                st.success(f"✅ Volume {volume_id} deleted successfully!")
                                log_command(f"AWS EBS: Deleted volume {volume_id}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                
                with col2:
                    if st.button("📸 Create Snapshot"):
                        description = st.text_input("Snapshot Description:", value=f"Snapshot of {volume_id}")
                        if st.button("📸 Create"):
                            try:
                                response = ec2_client.create_snapshot(
                                    VolumeId=volume_id,
                                    Description=description
                                )
                                snapshot_id = response['SnapshotId']
                                st.success(f"✅ Snapshot {snapshot_id} created successfully!")
                                log_command(f"AWS EBS: Created snapshot {snapshot_id}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                
                with col3:
                    if st.button("📊 Volume Info"):
                        try:
                            response = ec2_client.describe_volumes(VolumeIds=[volume_id])
                            volume = response['Volumes'][0]
                            
                            st.write(f"**Volume ID:** {volume['VolumeId']}")
                            st.write(f"**Size:** {volume['Size']} GB")
                            st.write(f"**Type:** {volume['VolumeType']}")
                            st.write(f"**State:** {volume['State']}")
                            st.write(f"**AZ:** {volume['AvailabilityZone']}")
                            st.write(f"**Encrypted:** {volume['Encrypted']}")
                            
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No volumes available. Please list volumes first.")
    
    with tab3:
        st.subheader("📸 EBS Snapshots")
        
        if st.button("📸 List Snapshots"):
            try:
                response = ec2_client.describe_snapshots(OwnerIds=['self'])
                snapshots = []
                
                for snapshot in response['Snapshots']:
                    snapshots.append({
                        'Snapshot ID': snapshot['SnapshotId'],
                        'Volume ID': snapshot['VolumeId'],
                        'Size (GB)': snapshot['VolumeSize'],
                        'State': snapshot['State'],
                        'Start Time': snapshot['StartTime'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Description': snapshot.get('Description', 'N/A')
                    })
                
                if snapshots:
                    df = pd.DataFrame(snapshots)
                    st.dataframe(df)
                    log_command(f"AWS EBS: Listed {len(snapshots)} snapshots")
                else:
                    st.info("No EBS snapshots found")
                    
            except Exception as e:
                st.error(f"Error listing snapshots: {e}")
