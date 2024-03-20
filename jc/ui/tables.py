import json
import django_tables2 as tables
from core import models


class ProviderTable(tables.Table):
    class Meta:
        model = models.Provider


class FlavorTable(tables.Table):
    class Meta:
        model = models.Flavor


class VectorTable(tables.Table):
    id = tables.Column()
    text = tables.Column()
    node_id = tables.Column()
    text_search_tsv = tables.Column()

    # metadata_ = tables.Column()

    def render_embedding(self, value):
        return bool(value)
