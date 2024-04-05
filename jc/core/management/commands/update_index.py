from django.core.management.base import BaseCommand, CommandError
from core.indices import IndexManager
from core.documents import DocumentManager
from core import utils


class Command(BaseCommand):
    help = """Update the index"""

    def add_arguments(self, parser):
        parser.add_argument('-m', '--embed-dim', type=int, default=384)
        parser.add_argument('-f', '--flush', action="store_true")

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])
        manager = IndexManager(
            verbose=options['verbosity'],
        )
        show_progress = options['verbosity'] > 2

        if options['flush']:
            self.stdout.write('Flushing index')
            manager.flush_indices()

        self.stdout.write('Updating indices')
        index = manager.update_indices(
        )
        self.stdout.write('Done')
