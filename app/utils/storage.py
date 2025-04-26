import logging
from boto3 import client as aws_s3_client
from botocore.exceptions import ClientError
import os

from app.core.config import settings


def get_aws_auth():
    return {
        'aws_access_key_id': settings.AWS_ACCESS_KEY,
        'aws_secret_access_key': settings.AWS_SECRET_KEY,
    }


def get_storage_client():
    auth = get_aws_auth()
    return aws_s3_client('s3', **auth)


def get_all_buckets():
    storage_client = get_storage_client()
    return storage_client.list_buckets()['Buckets']


def bucket_exists(bucket_name: str) -> bool:
    if not bucket_name:
        raise ValueError('Bucket name must be a non-empty string.')
    buckets = get_all_buckets()
    for bucket in buckets:
        if bucket_name == bucket['Name']:
            return True
    return False


def create_bucket(bucket_name: str):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :return: True if bucket created, else False
    """
    try:
        storage_client = get_storage_client()
        storage_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(
    *,
    file_name: str,
    bucket: str = settings.BUCKET_NAME,
    object_name: str | None = None,
):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    storage_client = get_storage_client()
    try:
        if not bucket_exists(bucket):
            create_bucket(bucket)
        response = storage_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(
    *,
    object_name: str,
    download_path: str,
    bucket: str = settings.BUCKET_NAME,
):
    storage_client = get_storage_client()
    with open(download_path, 'wb') as f:
        storage_client.download_fileobj(bucket, object_name, f)
