import boto3, subprocess
from datetime import datetime, timedelta

client = boto3.client('s3')
date_today = datetime.now().date()

backup_bucket = 'saif-timam-terraform'


def gimme_last_seven_days():
    days_of_last_week = []

    for day in range(0, 7):
        day = date_today - timedelta(days=day)
        days_of_last_week.append(str(day))

    return days_of_last_week


def gimme_list_of_apps():
    app_list = []

    bucket = 's3://' + backup_bucket + '/'
    all_apps = subprocess.check_output(['aws', 's3', 'ls', bucket]).decode('utf-8')

    raw_app_list = all_apps.split('/')

    for item in raw_app_list:
        date = item.replace('PRE ', '').lstrip()
        app_list.append(date)

    return app_list[:-1]


def gimme_list_of_backups(app_name):
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


def cleanup(cleanup_list):
    for item in cleanup_list:
        path = 's3://' + backup_bucket + '/' + app_name + '/' + item + '/'
        subprocess.check_output(['aws', 's3', 'rm', '--recursive', path])
        print("Cleanup Done : " + item)


def display_list_of_backups(app_name, list_of_backups):
    print("-" * 70)
    print(app_name + ' has ' + str(len(list_of_backups)) + ' backups')


def display_cleanup_message(cleanup_list):

    if len(cleanup_list) == 0:
        print("0 backup marked for cleanup")
    else:
        print(str(len(cleanup_list)) + " marked for backup \nclenaing up: " + str(cleanup_list))


last_seven_days = gimme_last_seven_days()
list_of_apps = gimme_list_of_apps()


for app_name in list_of_apps:

    list_of_backups = gimme_list_of_backups(app_name)
    display_list_of_backups(app_name, list_of_backups)

    cleanup_list = gimme_cleanup_list(last_seven_days, list_of_backups)
    display_cleanup_message(cleanup_list)

    cleanup(cleanup_list)
