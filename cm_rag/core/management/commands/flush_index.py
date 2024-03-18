from django.core.management.base import BaseCommand, CommandError
from core import indexes


class Command(BaseCommand):
    help = """Flush the Vector index"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        indexes.flush_index()
