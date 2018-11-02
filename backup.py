import boto3, subprocess
from datetime import datetime, timedelta


client = boto3.client('s3')
date_today = datetime.now().date()

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
        return 's3://' + backup_bucket + '/' + source_bucket + '-' + str(date_today) + '/'
    else:
        return 's3://' + backup_bucket + '/' + app_name + '/' + str(date_today) + '/'


def gimme_last_seven_days():
    days_of_last_week = []

    for day in range(0, 7):
        day = date_today - timedelta(days=day)
        days_of_last_week.append(str(day))

    return days_of_last_week


# Gathering Source and Destination Information
source = gimme_source()
destination = gimme_destination()

# BackingUp
subprocess.check_output(['aws', 's3', 'sync', source, destination])

# Gathering Backup Cleanup Information
last_seven_days = gimme_last_seven_days()
