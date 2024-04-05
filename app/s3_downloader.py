import boto3
import os

def download_from_s3(bucket_name, s3_object_key, local_file_path):
    """
    Downloads a single file from an S3 bucket to a local file path.

    :param bucket_name: Name of the S3 bucket.
    :param s3_object_key: Key of the object to download from the bucket.
    :param local_file_path: The local path to save the downloaded file.
    """
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, s3_object_key, local_file_path)
        print(f"Downloaded {s3_object_key} from S3 bucket {bucket_name} to {local_file_path}")
    except Exception as e:
        print(f"Failed to download {s3_object_key} from S3: {e}")

def download_files_from_s3(bucket_name, s3_object_keys, local_dir):
    """
    Downloads multiple files from an S3 bucket to a specified local directory.
    
    :param bucket_name: Name of the S3 bucket.
    :param s3_object_keys: List of S3 object keys to download.
    :param local_dir: Local directory to save the downloaded files.
    """
    for s3_object_key in s3_object_keys:
        # Extract filename from the S3 object key and construct local file path
        local_file_path = os.path.join(local_dir, os.path.basename(s3_object_key))
        download_from_s3(bucket_name, s3_object_key, local_file_path)
