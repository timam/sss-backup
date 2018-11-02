import boto3, subprocess
from time import gmtime, strftime

client = boto3.client('s3')
gimme_time = strftime("%Y-%m-%d-%H-%M", gmtime())

source_bucket = 'saif-cloudfront-test'
backup_bucket = 'saif-timam-terraform'

create_dir = client.put_object(
        Bucket=backup_bucket,
        Key=gimme_time+'/',
        )
source = 's3://'+source_bucket
destination = 's3://'+backup_bucket+'/'+gimme_time+'/'


subprocess.check_output(['aws', 's3', 'sync', '--delete', source, destination])

# seperare folder
# 7 days delete
# management server
# how long - lifecycle
