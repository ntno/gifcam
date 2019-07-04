import os, boto3, json, uuid
from twython import Twython
import boto3

TWITTER_APP_KEY='TWITTER_APP_KEY'
TWITTER_APP_SECRET='TWITTER_APP_SECRET'
TWITTER_OAUTH_TOKEN='TWITTER_OAUTH_TOKEN'
TWITTER_OAUTH_TOKEN_SECRET='TWITTER_OAUTH_TOKEN_SECRET'
TWITTER_MESSAGE='TWITTER_MESSAGE'

DEBUG=False

def getFileInfo(event):
  record = event['Records'][0]
  bucket = record['s3']['bucket']['name']
  key = record['s3']['object']['key']
  
  fileInfo = {}
  fileInfo['bucket'] = bucket
  fileInfo['key'] = key
  return fileInfo

def downloadFile(fileInfo):
  BUCKET_NAME = fileInfo['bucket']
  KEY = fileInfo['key']
  DOWNLOAD_PATH = '/tmp/{}'.format(str(uuid.uuid1()))

  s3Resource = boto3.resource('s3')
  gifBucket = s3Resource.Bucket(name=BUCKET_NAME)
  gifBucket.download_file(KEY, DOWNLOAD_PATH)

  fileInfo['local'] = DOWNLOAD_PATH
  return fileInfo

def getTwitterClient():
    APP_KEY = os.getenv(TWITTER_APP_KEY)
    APP_SECRET = os.getenv(TWITTER_APP_SECRET)
    OAUTH_TOKEN = os.getenv(TWITTER_OAUTH_TOKEN)
    OAUTH_TOKEN_SECRET = os.getenv(TWITTER_OAUTH_TOKEN_SECRET)

    #setup the twitter api client
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return twitter

def postToTwitter(filePath, statusMessage=os.getenv('TWITTER_MESSAGE', default="")):
  twitter = getTwitterClient()
  resp = None
  with open(filePath, 'rb') as img:
      if(DEBUG):
        return "tweet skipped due to DEBUG==True"
      else:
        twit_resp = twitter.upload_media(media=img)
        resp = twitter.update_status(status=statusMessage, media_ids=twit_resp['media_id'])
  return resp


def lambda_handler(event, context):    
    fileInfo = getFileInfo(event)
    fileInfo = downloadFile(fileInfo)
    fileInfo['twitter-response'] = postToTwitter(fileInfo['local'])

    response = {}
    response['statusCode'] = 200
    response['body'] = fileInfo
    return json.dumps(response)


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
          "key": "gifs/ntno.gif",
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
    DEBUG=True
    print(lambda_handler(TEST_EVENT, None))