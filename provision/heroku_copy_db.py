import boto3
import os
import subprocess
from django.conf import settings
from dotenv import load_dotenv


load_dotenv()

heroku_prod = "benefitmall"
heroku_prod_db_color = "HEROKU_POSTGRESQL_YELLOW"
heroku_dev = "benefitmall-dev"
heroku_dev_db_color = "DATABASE"


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

DEV_AWS_ACCESS_KEY_ID = os.getenv('DEV_AWS_ACCESS_KEY_ID')
DEV_AWS_SECRET_ACCESS_KEY = os.getenv('DEV_AWS_SECRET_ACCESS_KEY')
DEV_AWS_STORAGE_BUCKET_NAME = os.getenv('DEV_AWS_STORAGE_BUCKET_NAME')

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

client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def heroku_maint_mode(switch, heroku_env):
    print("   ***** Turning Maintenance Mode {} *****" .format(switch.upper()))
    maint = "heroku maintenance:{} -a {}".format(switch, heroku_env)
    subprocess.check_call(maint, shell=True)
    print('')

def heroku_copy_db(heroku_source_app, heroku_source_db_color, heroku_dest_app, heroku_dest_db_color):
    print("   ***** Copying the Database from {} to {} *****". format(heroku_source_app.upper(), heroku_dest_app.upper()))
    copy_db = "heroku pg:copy {}::{} {} -a {} --confirm {}".format(heroku_source_app, heroku_source_db_color, heroku_dest_db_color, heroku_dest_app, heroku_dest_app)
    subprocess.check_call(copy_db, shell=True)
    print('')

def db_migrate(heroku_dest_app):
    print("   ***** Running 'python manage.py migrate' on {} *****" .format(heroku_dest_app.upper()))
    migrate = "echo '/app/.heroku/python/bin/python /app/manage.py migrate && sleep 3 && exit' | heroku run bash --app {}" \
        .format(heroku_dest_app)
    subprocess.check_call(migrate, shell=True)
    print('')

def aws_sync_to_dest(heroku_dest_app, ACCESS_KEY_ID, SECRET_ACCESS_KEY, STORAGE_BUCKET_NAME):
    print("   ***** Sync'ing images to {} *****" .format(heroku_dest_app.upper()))
    aws_s3_sync = "AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} /usr/bin/aws s3 sync {} \
        s3://{} --acl public-read" .format(ACCESS_KEY_ID, SECRET_ACCESS_KEY, settings.MEDIA_ROOT,
                                           STORAGE_BUCKET_NAME)
    subprocess.check_call(aws_s3_sync, shell=True)
    print('')

heroku_maint_mode('on', heroku_dev)
heroku_copy_db(heroku_prod, heroku_prod_db_color, heroku_dev, heroku_dev_db_color)
db_migrate(heroku_dev)
download_dir(client, resource, '', settings.MEDIA_ROOT)
aws_sync_to_dest(heroku_dev, DEV_AWS_ACCESS_KEY_ID, DEV_AWS_SECRET_ACCESS_KEY, DEV_AWS_STORAGE_BUCKET_NAME)
heroku_maint_mode('off', heroku_dev)