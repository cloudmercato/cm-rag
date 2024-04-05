from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from core import utils
from core.qengines import SqlManager


class Command(BaseCommand):
    help = """Refresh database"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        utils.set_log_verbosity(options['verbosity'])

        sql_manager = SqlManager(
            verbose=options['verbosity'],
        )
        self.stdout.write("Refresh storage")
        sql_manager.build_index()

        for model_name, model in apps.all_models['core'].items():
            self.stdout.write("Refresh %s" % model_name)
            model.objects.refresh()
