import os
import logging
import boto3
import uuid
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv('BUCKET_NAME')
INPUT_PREFIX = os.getenv('INPUT_PREFIX')
OUTPUT_PREFIX = os.getenv('OUTPUT_PREFIX')

def getParent(key):
    pathList = key.rsplit('/')[0:-1]
    return '/'.join(pathList)

def getParentFolderName(key):
    return key.rsplit('/')[-2]


def getFileName(key):
    return key.rsplit('/')[-1]

def getFileInfo(event):
  record = event['Records'][0]
  bucket = record['s3']['bucket']['name']
  key = record['s3']['object']['key']
  parentKey = '{}/'.format(getParent(key))
  parentFolderName = getParentFolderName(key)

  fileInfo = {}
  fileInfo['bucket'] = bucket
  fileInfo['key'] = key
  fileInfo['parentKey'] = parentKey
  fileInfo['parentFolderName'] = parentFolderName
  return fileInfo

def getBucketResource(bucketName):
    s3Resource = boto3.resource('s3')
    bucket = s3Resource.Bucket(name=bucketName)
    return bucket

def downloadJpgsToTemp(fileInfo):
    bucketName = fileInfo['bucket']
    folderKey = fileInfo['parentKey']
    folderName = fileInfo['parentFolderName']

    downloadFolderPath = os.path.join('/tmp', folderName)
    if(not os.path.exists(downloadFolderPath)):
        os.mkdir(downloadFolderPath)

    bucket = getBucketResource(bucketName)

    # only download top level objects (no subfolders)
    for obj in bucket.objects.filter(Prefix = folderKey):
        #skip the 'folder' itself
        if(folderKey == obj.key):
            pass
        else:
            fileDownloadPath = os.path.join(downloadFolderPath, getFileName(obj.key))
            bucket.download_file(obj.key, fileDownloadPath)
    
    fileInfo['tmp'] = downloadFolderPath
    fileInfo['local-jpgs'] = '{}/*.jpg'.format(downloadFolderPath)
    fileInfo['local-gif'] = '{}/{}.gif'.format(downloadFolderPath, folderName)
    return fileInfo

def makeGif(fileInfo, gifDelay):
    gmCommand = 'gm convert -delay {} {} {}'.format(str(gifDelay), fileInfo['local-jpgs'], fileInfo['local-gif'])
    os.system(gmCommand)
    return fileInfo

def copyGifToS3(fileInfo):
    bucketName = fileInfo['bucket']
    bucket = getBucketResource(bucketName)

    fileInfo['gif-upload-path'] = '{}/{}.gif'.format(OUTPUT_PREFIX, fileInfo['parentFolderName'])

    try:
      uploadResponse = bucket.upload_file(fileInfo['local-gif'], fileInfo['gif-upload-path'], ExtraArgs={'ServerSideEncryption': 'AES256'})
      uploadResponse = 'uploaded without exception'
    except Exception as ex: 
      uploadResponse = str(ex)

    fileInfo['gif-upload-response'] = uploadResponse
    return fileInfo


def lambda_handler(event, context):  
    print(event)
    
    fileInfo = getFileInfo(event)
    print(fileInfo)

    fileInfo = downloadJpgsToTemp(fileInfo)
    print(fileInfo)

    fileInfo = makeGif(fileInfo, 15)
    print(fileInfo)

    fileInfo = copyGifToS3(fileInfo)
    print(fileInfo)

    return {'status':200, 'info': fileInfo}

TEST_EVENT = {
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-2",
      "eventTime": "2019-03-02T18:38:49.175Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "AWS:A2LPQ1GZ789FCU"
      },
      "requestParameters": {
        "sourceIPAddress": "108.97.23.193"
      },
      "responseElements": {
        "x-amz-request-id": "747F09J7D0D6E9DF",
        "x-amz-id-2": "XAmTajPHHFKAQ2gsd87IUaw3AXtYbohWplPgOl/oSga7dgDQmbT6Q059NmRHmYk46l7g5o="
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "5e223200-528c-4416-bf50-8c6e9af7efa8",
        "bucket": {
          "name": "picam",
          "ownerIdentity": {
            "principalId": "A2LPQ1GZ789FCU"
          },
          "arn": "arn:aws:s3:::picam"
        },
        "object": {
          "key": "jpgs/XYZ1234/sometimestamp.txt",
          "size": 47,
          "eTag": "de1b32cb27c6fb9svs3e8243521ce68",
          "versionId": "iZ1jK78k23MR29tkHXGNFFYaXO5",
          "sequencer": "005C7ACDBSD30A0E64CF"
        }
      }
    }
  ]
}

if __name__ == "__main__":
    lambda_handler(TEST_EVENT, None)