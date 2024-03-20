from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from core import utils


class Command(BaseCommand):
    help = """Refresh database"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])
        for model_name, model in apps.all_models['core'].items():
            self.stdout.write("Refresh %s" % model_name)
            model.objects.refresh()
