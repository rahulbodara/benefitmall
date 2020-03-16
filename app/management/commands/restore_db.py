import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Restore latest database dump'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', dest='force')

    def handle(self, *args, **options):
        if not options.get('force') :
            self.stdout.write(self.style.WARNING(
                    'This command is destructive and should not be run on '
                    'PRODUCTION. Are you sure?'
                )
            )
            confirm = input('Enter "YES" to confirm: ') # nosec
            if confirm != 'YES':
                return

        os.system('dropdb stack_theme')  # nosec
        os.system('createdb stack_theme')  # nosec
        os.system('pg_restore --clean --if-exists --no-acl --no-owner -d stack_theme latest.dump')  # nosec
        # Re-own all of the stuff, so it won't give errors on save

        self.stdout.write(self.style.SUCCESS(
                'DONE'
            )
        )
