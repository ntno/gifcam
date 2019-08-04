import logging
import boto3
from botocore.exceptions import ClientError

S3_CLIENT = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = S3_CLIENT.upload_file(file_name, bucket, object_name, ExtraArgs={'ServerSideEncryption': 'AES256'})
        logging.info(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    upload_file('./gifs/ntno.gif', 'ntno-picam', 'gifs/ntno.gif')