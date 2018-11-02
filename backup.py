import boto3, subprocess
from time import gmtime, strftime

client = boto3.client('s3')
gimme_time = strftime("%Y-%m-%d-%H-%M", gmtime())
app_name = ''

source_bucket = 'saif-cloudfront-test'
backup_bucket = 'saif-timam-terraform'


def gimme_source():
    if not app_name:
        return 's3://' + source_bucket
    else:
        return 's3://' + source_bucket + '/' + app_name


def gimme_destination():
    if not app_name:
        return 's3://' + backup_bucket + '/' + source_bucket + '-' + gimme_time + '/'
    else:
        return 's3://' + backup_bucket + '/' + app_name + '/' + gimme_time + '/'


source = gimme_source()
destination = gimme_destination()

subprocess.check_output(['aws', 's3', 'sync', '--delete', source, destination])


