import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('db available!'))
