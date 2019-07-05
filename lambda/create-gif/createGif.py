import os
import logging
import boto3
import uuid
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
PUT_PREFIX = os.getenv('PUT_PREFIX')
URL_TIMEOUT = os.getenv('URL_TIMEOUT')

S3_CLIENT = boto3.client('s3')

def generateFileName():
    return '{}.gif'.format(str(uuid.uuid1()))

def create_presigned_url(bucket_name=BUCKET_NAME, object_name=generateFileName(), expiration=URL_TIMEOUT):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = S3_CLIENT.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': '{}{}'.format(PUT_PREFIX, object_name)},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response



def lambda_handler(event, context):  
    presignedUrl = str(create_presigned_url())
    return {'status':200, 'url': presignedUrl}

if __name__ == "__main__":
    DEBUG=True
    print(lambda_handler(None, None))