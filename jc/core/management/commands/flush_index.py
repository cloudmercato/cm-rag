from django.core.management.base import BaseCommand, CommandError
from core.storage import StorageManager
from core import utils


class Command(BaseCommand):
    help = """Flush the Vector index"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])
        manager = StorageManager(
            verbose=options['verbosity'],
        )
        self.stdout.write('Flushing index')
        manager.flush()
