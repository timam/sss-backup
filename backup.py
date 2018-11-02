import boto3, subprocess
from time import strftime


client = boto3.client('s3')
date_today = strftime("%Y-%m-%d")

app_name = 'swin'

source_bucket = 'saif-cloudfront-test'
backup_bucket = 'saif-timam-terraform'


def gimme_source():
    if not app_name:
        return 's3://' + source_bucket + '/'
    else:
        return 's3://' + source_bucket + '/' + app_name + '/'


def gimme_destination():
    if not app_name:
        return 's3://' + backup_bucket + '/' + source_bucket + '-' + date_today + '/'
    else:
        return 's3://' + backup_bucket + '/' + app_name + '/' + date_today+ '/'


source = gimme_source()
destination = gimme_destination()

subprocess.check_output(['aws', 's3', 'sync', source, destination])
