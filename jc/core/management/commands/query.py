import sys
import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core import utils


DEFAULT_QUERY = "What is the top 3 data you can retrieve about price and performance for each provider?"
QENGINES_CHOICES = (
    'router',
    'subquestion',
    'recursive-retriever',
    'vector',
    'sql',
    'sql-retriever',
    'kg',
    'kg-retriever',
)


class Command(BaseCommand):
    help = """Query the model"""

    def add_arguments(self, parser):
        parser.add_argument('-m', '--embed-dim', type=int, default=settings.DEFAULT_EMBED_DIM)
        parser.add_argument('-o', '--ollama-model', default=settings.DEFAULT_OLLAMA_MODEL)
        parser.add_argument('-q', '--query', default=DEFAULT_QUERY)
        parser.add_argument('-Q', '--query-engine', default='router', choices=QENGINES_CHOICES)
        parser.add_argument('-s', '--similarity-top-k', type=int, default=settings.DEFAULT_SIMILARITY_TOP_K)
        parser.add_argument('-t', '--temperature', type=float, default=settings.DEFAULT_TEMPERATURE)

    def handle(self, *args, **options):
        logging.basicConfig(stream=sys.stdout, level=40-options['verbosity']*10)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

        query_engine = utils.get_query_engine(
            embed_dim=options['embed_dim'],
            ollama_model=options['ollama_model'],
            query_engine=options['query_engine'],
            similarity_top_k=options['similarity_top_k'],
            temperature=options['temperature'],
            verbose=options['verbosity']>1,
        )
        response = query_engine.query(options['query'])
        print('\n\n')
        print(f"< {options['query']}")
        print(f"> {response.response}")
