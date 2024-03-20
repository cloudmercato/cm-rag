from django.core.management.base import BaseCommand, CommandError
from core.qengines import VectorIndexManager
from core import documents
from core import utils


class Command(BaseCommand):
    help = """Update the index"""

    def add_arguments(self, parser):
        parser.add_argument('-m', '--embed-dim', type=int, default=384)
        parser.add_argument('-f', '--flush', action="store_true")

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])
        manager = VectorIndexManager(
            embed_dim=options['embed_dim'],
            verbose=options['verbosity'],
        )
        show_progress = options['verbosity'] > 2

        if options['flush']:
            self.stdout.write('Flushing index')
            manager.flush_index()

        docs, nodes = documents.DocumentManager().get_documents()
        self.stdout.write('Updating index')
        index = manager.update_index(
            documents=docs,
        )
        self.stdout.write('Done')
