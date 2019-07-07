import os, logging, boto3, uuid, requests, copy, json
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
PUT_PREFIX = os.getenv('PUT_PREFIX')
# URL_TIMEOUT = os.getenv('URL_TIMEOUT')

S3_CLIENT = boto3.client('s3')
LOGGER = logging.getLogger(__name__)

def generateFolderName():
    return '{}'.format(str(uuid.uuid1()))

def generateS3Prefix(folderName):
    return '{}/{}/'.format(PUT_PREFIX, folderName)

def getFields():
    return {'x-amz-server-side-encryption': "AES256"}

def getConditions(keyPrefix):
    serverSideEncryption = {"x-amz-server-side-encryption":"AES256"}
    prefix = ["starts-with", "$key", keyPrefix]
    conditions = [prefix, serverSideEncryption]
    return conditions

def create_presigned_post(object_name, bucket_name=BUCKET_NAME,
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
        objectKey = '{}{}'.format(conditions[0][2], object_name)
        response = s3_client.generate_presigned_post(bucket_name,
                                                     objectKey,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        LOGGER.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def postToPresignedUrl(url, fields, pathToFile):
    with open(pathToFile, 'rb') as f:
        # s3Key = '{}'.format(fields['key'])
        files = {'file': ("somestring", f)}
        http_response = requests.post(url, data=fields, files=files)
    # files = {'file': open(pathToFile, 'rb')}
    # http_response = requests.post(url, data=fields, files=files)
    return http_response

#you can use the same URL twice to load two different files (but they get saved to the same key)
def testPresignedUrl(pathToFile):
    folderName = generateFolderName()
    s3FilePrefix = generateS3Prefix(folderName)
    postConditions = getConditions(s3FilePrefix)

    presigned = create_presigned_post("test-0.txt", fields=getFields(), conditions=postConditions)
    LOGGER.error(json.dumps(presigned))

    httpResponse = postToPresignedUrl(presigned['url'], presigned['fields'], pathToFile)
    LOGGER.error(httpResponse.status_code)
    httpResponse.close()

    anotherResponse = postToPresignedUrl(presigned['url'], presigned['fields'], "boto3_examples.py")
    LOGGER.error(anotherResponse.status_code)
    anotherResponse.close()

def lambda_handler(event, context):
    # filename = generatePrefi  x()
    presignedUrl = 'yolo'

    testPresignedUrl("generateUrl.py")
    # str(create_presigned_url(generateFileName))
    # print(presignedUrl)
    # testUrl(presignedUrl)
    return {'status':200} #, 'url': presignedUrl, 'filename' : filename, 'timeout':URL_TIMEOUT}

if __name__ == "__main__":
    DEBUG=True
    print(lambda_handler(None, None))