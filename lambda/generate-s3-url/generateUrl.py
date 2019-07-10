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

def generateFields():
    return {'x-amz-server-side-encryption': "AES256"}

def generateConditions(keyPrefix):
    serverSideEncryption = {"x-amz-server-side-encryption":"AES256"}
    prefix = ["starts-with", "$key", keyPrefix]
    return [prefix, serverSideEncryption]


def create_presigned_post(objectKey, conditions, bucketName=BUCKET_NAME, expiration=3600):
    # Generate a presigned S3 POST URL
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


def createPresignedUrls(fileNames, bucketName):
    randomFolderName = generateFolderName()
    s3FolderKey = generateS3Prefix(randomFolderName)
    
    urls = []
    for fn in fileNames:
        objectKey = '{}{}'.format(s3FolderKey, fn)
        urlResponse = create_presigned_post(objectKey, generateConditions(s3FolderKey))
        urls.append(urlResponse)
    return urls

def postToPresignedUrl(urlResponse, pathToFile):
    with open(pathToFile, 'rb') as f:
        files = {'file': (pathToFile, f)}
        http_response = requests.post(urlResponse['url'], data=urlResponse['fields'], files=files)
    return http_response


#you can use the same URL twice to load two different files (but they get saved to the same key)
def testPresignedUrl(pathToFile):
    resp = createPresignedUrls(["a", "b", "d"], BUCKET_NAME)
    LOGGER.error(resp)

    idx=0
    for fn in ["boto3_examples.py", "generateUrl.py", "presignedPostExample.py"]:
        postToPresignedUrl(resp[idx], fn)
        idx = idx+1


def lambda_handler(event, context):
    print("EVENT")
    print(event)

    print("CONTEXT")
    print(context)
    
    return {'status':200, 'event':event, 'context':context}

if __name__ == "__main__":
    DEBUG=True
    print(lambda_handler(None, None))