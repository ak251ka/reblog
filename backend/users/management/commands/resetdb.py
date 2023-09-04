"""
this command is in development, it will be used to reset the database
and create a new superuser, new database
"""

from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'reset database'

    def handle(self, *args, **options):
        """this function resets the database

        Raises:
            CommandError: if It is not in development mode
            CommandError: if there is an error in the database
        """
        if not settings.DEBUG:
            raise CommandError(
                'This command can only be run in development mode.'
            )
        try:
            with connection.cursor() as cursor:
                cursor.execute('SET CONSTRAINTS ALL IMMEDIATE;')
                cursor.execute('DROP SCHEMA public CASCADE;')
                cursor.execute('CREATE SCHEMA public;')
            call_command('makemigrations')
            call_command('migrate')
            call_command('createcachetable')
            self.stdout.write(self.style.NOTICE('Creating supper user!'))
            call_command('createsuperuser')

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully reset database!')
            )

        except Exception as e:
            error_message = str(e)
            raise CommandError(error_message)
