import boto3, subprocess
from datetime import datetime


source_bucket = 'saif-cloudfront-test'
backup_bucket = 'saif-timam-terraform'


def gimme_list_of_apps():
    app_list = []

    bucket = 's3://' + source_bucket + '/'
    all_apps = subprocess.check_output(['aws', 's3', 'ls', bucket]).decode('utf-8')

    raw_app_list = all_apps.split('/')

    for item in raw_app_list:
        date = item.replace('PRE ', '').lstrip()
        app_list.append(date)

    return app_list[:-1]


def gimme_source(app_name):
    return 's3://' + source_bucket + '/' + app_name + '/'


def gimme_destination(app_name):
    return 's3://' + backup_bucket + '/' + app_name + '/' + str(date_today) + '/'


def display_generic_message():
    print("Today is : " + str(date_today))
    print(str(len(list_of_apps)) + " application form bucket " + source_bucket + " marked for backup")


def display_backing_up_message():
    print('-' * 70 + "\nBacking Up : " + source_bucket + '/' + app_name)


def display_backup_compilation_message():
    print("Backup Completed : " + app_name)
    print("Backup Available on : " + destination + "\n" + '-' * 70)


list_of_apps = gimme_list_of_apps()
date_today = datetime.now().date()

display_generic_message()

for app_name in list_of_apps:

    source = gimme_source(app_name)
    destination = gimme_destination(app_name)

    display_backing_up_message()

    subprocess.check_output(['aws', 's3', 'sync', source, destination])

    display_backup_compilation_message()
