import os

from llama_index.core.storage.index_store.simple_index_store import SimpleIndexStore
from llama_index.storage.index_store.postgres import PostgresIndexStore

from django.conf import settings
from django.utils.functional import cached_property

from core.storage.base import BaseSqlManager


class IndexStoreManager(BaseSqlManager):
    @cached_property
    def index_persist_dir(self):
        persist_path = os.path.join(settings.STORAGE_DIR, 'index')
        return persist_path

    @cached_property
    def index_persist_path(self):
        persist_path = os.path.join(self.index_persist_dir, 'index-store.json')
        return persist_path

    @cached_property
    def local_index_store(self):
        try:
            return SimpleIndexStore.from_persist_dir(
                persist_dir=self.index_persist_dir,
            )
        except FileNotFoundError as err:
            return SimpleIndexStore()

    @cached_property
    def index_store(self):
        return PostgresIndexStore.from_params(
            **self.pg_params
        )

    @cached_property
    def store(self):
        return self.index_store
