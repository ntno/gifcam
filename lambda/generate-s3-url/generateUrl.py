import os, logging, boto3, uuid, requests, copy, json
from pathlib import Path
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
PUT_PREFIX = os.getenv('PUT_PREFIX')
# URL_TIMEOUT = os.getenv('URL_TIMEOUT')

S3_CLIENT = boto3.client('s3')
LOGGER = logging.getLogger(__name__)

def generateRandomFileName():
    return '{}{}'.format(str(uuid.uuid1()), '.jpg')

def generateS3Prefix(fileName):
    return '{}/{}'.format(PUT_PREFIX, fileName)

def generateFields():
    return {'x-amz-server-side-encryption': "AES256"}

def generateConditions(expectedKey):
    serverSideEncryption = {"x-amz-server-side-encryption":"AES256"}
    prefix = ["starts-with", "$key", expectedKey]
    return [prefix, serverSideEncryption]


def generatePresignedPostUrl(objectKey, bucketName=BUCKET_NAME, expiration=3600):
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
    LOGGER.warning("EVENT")
    LOGGER.warning(event)
    
    return {'status':200, 'event':event}

if __name__ == "__main__":
    presigned = getPresignedPostUrl('kermit.jpg')
    print(presigned)

    numFrames = 21
    frames = []
    for i in range(0, numFrames):
        pathToFrame = os.path.join('../../jpgs/frames/', str(i) + '.jpg')
        frames.append(Path(pathToFrame))
    for p in frames:
        response = postToPresignedUrl(presigned, p)
        print(response.status_code)