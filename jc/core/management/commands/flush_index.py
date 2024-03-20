from django.core.management.base import BaseCommand, CommandError
from core.qengines import VectorIndexManager
from core import utils


class Command(BaseCommand):
    help = """Flush the Vector index"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])
        manager = VectorIndexManager(
            verbose=options['verbosity'],
        )
        self.stdout.write('Flushing index')
        manager.flush_index()
