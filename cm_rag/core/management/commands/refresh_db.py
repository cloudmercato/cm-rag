import sys
import logging

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = """Query the model"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(stream=sys.stdout, level=40-options['verbosity']*10)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

        for model_name, model in apps.all_models['core'].items():
            self.stdout.write("Refresh %s" % model_name)
            model.objects.refresh()
