import os
import boto3

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from dotenv import load_dotenv
load_dotenv()
# import environ
# env = environ.Env()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')


def download_dir(client, resource, dist, local='/tmp', bucket=AWS_STORAGE_BUCKET_NAME): # nosec
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        if result.get('Contents') is not None:
            for file in result.get('Contents'):
                if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
                    os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
                print(local + os.sep + file.get('Key'))
                resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))


class Command(BaseCommand):
    help = 'Restore media from s3'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', dest='force')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
                'This command is destructive and should not be run on '
                'PRODUCTION. Are you sure?'
            )
        )
        confirm = input('Enter "YES" to confirm: ')  #nosec
        if confirm != 'YES':
            return

        client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        download_dir(client, resource, '', settings.MEDIA_ROOT)

        self.stdout.write(self.style.SUCCESS(
                'DONE'
            )
        )
