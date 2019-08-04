#https://github.com/boto/boto3/issues/934
#author: subhankarb on github

import boto3
import requests
import os

bucket_name = os.getenv("BUCKET_NAME")
key = '934/example.py'
local_path='generateUrl.py'

s3_client = boto3.client('s3')
presigned = s3_client.generate_presigned_post(  Bucket=bucket_name,
                                            Key=key,
                                            Fields={
                                            'x-amz-server-side-encryption': "AES256",
                                            'Content-Type': 'text/plain'
                                            },
                                            Conditions=[
                                                {"x-amz-server-side-encryption":"AES256"},
                                                ["starts-with", "$Content-Type", ""],     #content-type must be specified, but can start with any string
                                                ["starts-with", "$key", "934/"]
                                            ]
                                        )

url = presigned['url']
fields = presigned['fields']
files = {'file': open(local_path, 'rb')}
response = requests.post(url, data=fields, files=files)
print(response)
