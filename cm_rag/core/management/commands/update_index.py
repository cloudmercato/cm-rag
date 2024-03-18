import sys
import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core import indexes
from core import documents


class Command(BaseCommand):
    help = """Update the index"""

    def add_arguments(self, parser):
        parser.add_argument('-m', '--embed-dim', type=int, default=384)
        parser.add_argument('-f', '--flush', action="store_true")

    def handle(self, *args, **options):
        logging.basicConfig(stream=sys.stdout, level=40-options['verbosity']*10)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
        show_progress = options['verbosity'] > 2

        if options['flush']:
            indexes.flush_index()

        docs, nodes = documents.DocumentManager().get_documents()
        index = indexes.VectorIndexManager().update_index(
            documents=docs,
            embed_dim=options['embed_dim'],
            show_progress=show_progress,
        )
