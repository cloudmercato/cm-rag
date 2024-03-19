import django_tables2 as tables
from core import models


class ProviderTable(tables.Table):
    class Meta:
        model = models.Provider


class FlavorTable(tables.Table):
    class Meta:
        model = models.Flavor
