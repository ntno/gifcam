import os
import logging
import boto3
import uuid
import requests
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
PUT_PREFIX = os.getenv('PUT_PREFIX')
URL_TIMEOUT = os.getenv('URL_TIMEOUT')

S3_CLIENT = boto3.client('s3')

def generateFileName():
    return '{}.gif'.format(str(uuid.uuid1()))

def create_presigned_post(bucket_name=BUCKET_NAME, object_name=generateFileName(),
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        # if(not fields):
        #     fields={}
        # fields['s3:x-amz-server-side-encryption']='AES256'
        # print("generating with fields=", fields)
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def testPresignedUrl():
    filename = generateFileName()
    response = create_presigned_post(object_name=filename)
    if response is None:
        print("could not generate url")
    else:
        print("url", response['url'])
        print("fields", response['fields'])
        with open('test.txt', 'rb') as f:
            files = {'file': (filename, f)}
            http_response = requests.post(response['url'], data=response['fields'], files=files)
        # If successful, returns HTTP status code 204
        print(f'File upload HTTP status code: {http_response.status_code}')


def lambda_handler(event, context):  
    filename = generateFileName()
    presignedUrl = 'yolo'

    testPresignedUrl()
    # str(create_presigned_url(generateFileName))
    # print(presignedUrl)
    # testUrl(presignedUrl)
    return {'status':200, 'url': presignedUrl, 'filename' : filename, 'timeout':URL_TIMEOUT}

if __name__ == "__main__":
    DEBUG=True
    print(lambda_handler(None, None))