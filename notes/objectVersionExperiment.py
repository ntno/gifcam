import boto3

s3 = boto3.client('s3')
bucket_name = 'BUCKET_NAME'
versions = s3.list_object_versions (Bucket = bucket_name, Prefix = 'kermit/kermit.gif')

for v in versions['Versions']:
    print ('id: {}, latest: {}'.format(v['VersionId'], v['IsLatest']))
