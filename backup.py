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


def display_backing_up_message():
    print('='*50 +"\nToday is : " + str(date_today))
    print("Taking backup of : " + app_name)


def display_backup_success_message():
    print('='*50 +"\nBackup for " + app_name + " is completed")
    print("Backup is available on : " + destination)


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


def gimme_list_of_backups():
    backup_list = []

    app_path = 's3://' + backup_bucket + '/' + app_name + '/'
    all_backups = subprocess.check_output(['aws', 's3', 'ls', app_path]).decode('utf-8')

    raw_backup_list = all_backups.split('/')

    for item in raw_backup_list:
        date = item.replace('PRE ', '').lstrip()
        backup_list.append(date)

    return backup_list[:-1]


def gimme_cleanup_list(last_seven_days, list_of_backups):
    cleanup = list(set(list_of_backups) - set(last_seven_days))

    return cleanup


def display_cleanup_message(cleanup_list):
    if len(cleanup_list) == 0 :
        print('='*50 + "\nIdentified " + str(len(cleanup_list)) + " backup for cleanup")
        print("Nothing to do...")
    else:
        print('='*50 + "\nIdentified " + str(len(cleanup_list)) + " backup for cleanup")
        print("Cleaning Up : " + str(cleanup_list))



# Gathering Source and Destination Information
source = gimme_source()
destination = gimme_destination()

# BackingUp
display_backing_up_message()
subprocess.check_output(['aws', 's3', 'sync', source, destination])
display_backup_success_message()

# Gathering Backup Cleanup Information
last_seven_days = gimme_last_seven_days()
list_of_backups = gimme_list_of_backups()
cleanup_list = gimme_cleanup_list(last_seven_days, list_of_backups)

display_cleanup_message(cleanup_list)

for item in cleanup_list:
    path = 's3://' + backup_bucket + '/' + app_name + '/' + item + '/'
    subprocess.check_output(['aws', 's3', 'rm', '--recursive', path])
    print("Cleanup Done : " + item)

