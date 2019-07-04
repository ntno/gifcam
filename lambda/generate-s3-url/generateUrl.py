import os, boto3, time, logging
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
PUT_PREFIX = os.getenv('PUT_PREFIX')
URL_TIMEOUT = os.getenv('URL_TIMEOUT')

S3_CLIENT = boto3.client('s3')

def generateFileName():
    return '{}.gif'.format(time.time_ns())

def create_presigned_url(bucket_name, object_name=generateFileName(), expiration=URL_TIMEOUT):
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
    print(event)
    return {'status':200}

if __main__