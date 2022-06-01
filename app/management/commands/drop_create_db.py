import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Restore latest database dump'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', dest='force')

    def handle(self, *args, **options):
        if not options.get('force'):
            self.stdout.write(self.style.WARNING(
                    'This command is destructive and should not be run on '
                    'PRODUCTION. Are you sure?'
                )
            )
            confirm = input('Enter "YES" to confirm: ')  # nosec
            if confirm != 'YES':
                return

        os.system('dropdb stack_theme')  # nosec
        os.system('createdb stack_theme')  # nosec

        self.stdout.write(self.style.SUCCESS(
                'DONE'
            )
        )
