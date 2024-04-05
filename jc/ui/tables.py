import json

from django.urls import reverse
from django.utils.safestring import mark_safe

import django_tables2 as tables

from core import models


class ProviderTable(tables.Table):
    class Meta:
        model = models.Provider


class FlavorTable(tables.Table):
    class Meta:
        model = models.Flavor


class IndexTable(tables.Table):
    id = tables.Column()
    key = tables.Column()
    namespace = tables.Column()

    def render_key(self, value):
        href = reverse('index-detail', args=[value])
        tag = f'<a href="{href}">{value}</a>'
        return mark_safe(tag)


class VectorTable(tables.Table):
    id = tables.Column()
    text = tables.Column()
    node_id = tables.Column()
    text_search_tsv = tables.Column()

    def render_id(self, value):
        href = reverse('vector-detail', args=[value])
        tag = f'<a href="{href}">{value}</a>'
        return mark_safe(tag)


class DocumentTable(tables.Table):
    id = tables.Column()
    key = tables.Column()
    namespace = tables.Column()

    def render_key(self, value):
        href = reverse('document-detail', args=[value])
        tag = f'<a href="{href}">{value}</a>'
        return mark_safe(tag)
