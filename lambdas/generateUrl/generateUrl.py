import os, logging, boto3, uuid, requests, copy, json
from pathlib import Path
from botocore.exceptions import ClientError

#global constants
BUCKET_NAME=None
INPUT_PREFIX=None
URL_RESPONSE_TOPIC=None
LOG_LEVEL=None
URL_TIMEOUT=None
AWS_REGION=None

#global resources
S3_CLIENT=None
IOT_DATA_CLIENT=None
LOGGER=None

def setUpConstants(retrieveFromEnvironment=True):
    global BUCKET_NAME, INPUT_PREFIX, URL_RESPONSE_TOPIC, LOG_LEVEL, URL_TIMEOUT, AWS_REGION
    if(retrieveFromEnvironment):
        BUCKET_NAME = os.getenv('BUCKET_NAME')
        INPUT_PREFIX = os.getenv('INPUT_PREFIX')
        URL_RESPONSE_TOPIC = os.getenv('URL_RESPONSE_TOPIC')
        LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
        URL_TIMEOUT = int(os.getenv('URL_TIMEOUT'))
        AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-2')
    else:
        BUCKET_NAME='ntno-picam'
        INPUT_PREFIX='jpgs'
        URL_RESPONSE_TOPIC='presigned-url'
        LOG_LEVEL='DEBUG'
        URL_TIMEOUT=30
        AWS_REGION='us-east-2'

def initializeResources():
    global S3_CLIENT, IOT_DATA_CLIENT, LOGGER
    S3_CLIENT=boto3.client('s3', AWS_REGION)
    IOT_DATA_CLIENT = boto3.client('iot-data', AWS_REGION)
    LOGGER = logging.getLogger(__name__)

def generateRandomFileName():
    return '{}{}'.format(str(uuid.uuid1()), '.jpg')

def generateS3Prefix(fileName):
    return '{}/{}'.format(INPUT_PREFIX, fileName)

def generateFields():
    return {'x-amz-server-side-encryption': "AES256"}

def generateConditions(expectedKey):
    serverSideEncryption = {"x-amz-server-side-encryption":"AES256"}
    prefix = ["starts-with", "$key", expectedKey]
    return [prefix, serverSideEncryption]

def generatePresignedPostUrl(objectKey, bucketName, expiration):
    # Generate a presigned S3 POST URL
    conditions = generateConditions(objectKey)
    fields = generateFields()
    try:
        response = S3_CLIENT.generate_presigned_post(bucketName,
                                                     objectKey,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        LOGGER.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

# #you can use the same URL twice to load two different files (but they get saved to the same key)
def postToPresignedUrl(urlResponse, pathToFile):
    http_response = requests.post(urlResponse['url'], data=urlResponse['fields'], files={'file': open(pathToFile, 'rb')})
    return http_response

def generatePresignedDeleteUrl(objectKey, bucketName, expiration):
    # Generate a presigned S3 DELETE URL
    try:
        response = S3_CLIENT.generate_presigned_url(ClientMethod='delete_object',
                                                    Params={'Bucket': bucketName, 'Key':objectKey},
                                                    ExpiresIn=expiration,
                                                    HttpMethod='DELETE')
    except ClientError as e:
        LOGGER.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def deleteToPresignedUrl(url):
    http_response = requests.delete(url)
    return http_response

def lambda_handler(event, context):
    setUpConstants()
    initializeResources()

    LOGGER.setLevel(LOG_LEVEL)
    LOGGER.info(event)
    
    presignedUrlResponse = None
    if(event.get('fileName') != None):
        presignedUrlResponse = generatePresignedPostUrl(generateS3Prefix(event.get('fileName')), bucketName=BUCKET_NAME, expiration=URL_TIMEOUT)
    else:
        presignedUrlResponse = generatePresignedPostUrl(generateS3Prefix(generateRandomFileName()), bucketName=BUCKET_NAME, expiration=URL_TIMEOUT)

    if(event.get('info') != None):
        presignedUrlResponse['info'] = event.get('info')

    LOGGER.info(presignedUrlResponse)
    IOT_DATA_CLIENT.publish(topic=URL_RESPONSE_TOPIC, qos=0, payload=json.dumps(presignedUrlResponse))

    return {'status':200, 'event':event, 'presigned' : presignedUrlResponse}

if __name__ == "__main__":
    setUpConstants(retrieveFromEnvironment=False)
    initializeResources()
    LOGGER.setLevel(LOG_LEVEL)

    fileName='kermit-4.jpg'
    presigned = generatePresignedPostUrl(generateS3Prefix(fileName), bucketName=BUCKET_NAME, expiration=URL_TIMEOUT)
    print("PRESIGNED POST", presigned)

    numFrames = 21
    frames = []
    for i in range(0, numFrames):
        pathToFrame = os.path.join('../../jpgs/frames/', str(i) + '.jpg')
        frames.append(Path(pathToFrame))
    for p in frames:
        response = postToPresignedUrl(presigned, p)
        print(p, response.status_code)

    presigned = generatePresignedDeleteUrl(generateS3Prefix(fileName), bucketName=BUCKET_NAME, expiration=URL_TIMEOUT)
    print("PRESIGNED DELETE", presigned)
    deleteResponse = deleteToPresignedUrl(presigned)
    print(deleteResponse)
