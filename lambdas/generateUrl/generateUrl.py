import os, logging, boto3, uuid, requests, copy, json
from pathlib import Path
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
INPUT_PREFIX = os.getenv('INPUT_PREFIX')
URL_RESPONSE_TOPIC = os.getenv('URL_RESPONSE_TOPIC')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
URL_TIMEOUT = int(os.getenv('URL_TIMEOUT'))
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-2')

S3_CLIENT = boto3.client('s3', AWS_REGION)
IOT_DATA_CLIENT = boto3.client('iot-data', AWS_REGION)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)

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


def generatePresignedPostUrl(objectKey, bucketName=BUCKET_NAME, expiration=URL_TIMEOUT):
    # Generate a presigned S3 POST URL
    conditions = generateConditions(objectKey)
    try:
        response = S3_CLIENT.generate_presigned_post(bucketName,
                                                     objectKey,
                                                     Fields=generateFields(),
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        LOGGER.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def getPresignedPostUrl(fileName=generateRandomFileName(), bucketName=BUCKET_NAME):
    s3Key = generateS3Prefix(fileName)
    urlResponse = generatePresignedPostUrl(s3Key)
    return urlResponse

# #you can use the same URL twice to load two different files (but they get saved to the same key)
def postToPresignedUrl(urlResponse, pathToFile):
    http_response = requests.post(urlResponse['url'], data=urlResponse['fields'], files={'file': open(pathToFile, 'rb')})
    return http_response

def lambda_handler(event, context):
    LOGGER.info(event)
    
    presignedUrlResponse = None
    if(event.get('fileName') != None):
        presignedUrlResponse = getPresignedPostUrl(fileName=event.get('fileName'))
    else:
        presignedUrlResponse = getPresignedPostUrl()

    if(event.get('info') != None):
        presignedUrlResponse['info'] = event.get('info')

    LOGGER.info(presignedUrlResponse)
    IOT_DATA_CLIENT.publish(topic=URL_RESPONSE_TOPIC, qos=0, payload=json.dumps(presignedUrlResponse))

    return {'status':200, 'event':event, 'presigned' : presignedUrlResponse}

if __name__ == "__main__":
    presigned = getPresignedPostUrl(fileName='kermit.jpg')
    print(presigned)

    numFrames = 21
    frames = []
    for i in range(0, numFrames):
        pathToFrame = os.path.join('../../jpgs/frames/', str(i) + '.jpg')
        frames.append(Path(pathToFrame))
    for p in frames:
        response = postToPresignedUrl(presigned, p)
        print(p, response.status_code)