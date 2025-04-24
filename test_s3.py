import os
import boto3
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

def test_s3_connection():
    print("Testing S3 connection...")
    
    # Get the region name directly
    region_name = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-2')
    print(f"Using region: {region_name}")
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=region_name
    )
    
    # List buckets to test connection
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print(f"Connected to S3. Available buckets: {buckets}")
    
    # Check if our bucket exists
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    if bucket_name in buckets:
        print(f"Bucket '{bucket_name}' found!")
    else:
        print(f"Bucket '{bucket_name}' not found! Check your bucket name.")
    
    return s3

def upload_test_file(s3):
    print("\nUploading test file...")
    # Create a test file
    test_file_path = 'test_upload.txt'
    with open(test_file_path, 'w') as f:
        f.write('This is a test file for S3 upload.')
    
    bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    
    # Upload to S3
    try:
        s3.upload_file(
            test_file_path, 
            bucket_name, 
            'media/test222.txt',
            ExtraArgs={'ACL': 'public-read'}
        )
        print("Test file uploaded successfully!")
        
        # Get the URL
        region = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-2')
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/media/test222.txt"
        print(f"File should be accessible at: {url}")
        
        # Clean up local file
        os.remove(test_file_path)
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    s3_client = test_s3_connection()
    upload_test_file(s3_client)