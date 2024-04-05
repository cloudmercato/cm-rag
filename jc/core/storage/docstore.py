import os

from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.storage.docstore.postgres import PostgresDocumentStore

from django.conf import settings
from django.utils.functional import cached_property

from core.storage.base import BaseSqlManager


class DocstoreManager(BaseSqlManager):
    @cached_property
    def doc_persist_dir(self):
        persist_path = os.path.join(settings.STORAGE_DIR, 'docs')
        return persist_path

    @cached_property
    def doc_persist_path(self):
        persist_path = os.path.join(self.doc_persist_dir, 'docstore.json')
        return persist_path

    @cached_property
    def local_docstore(self):
        try:
            return SimpleDocumentStore.from_persist_dir(
                persist_dir=self.doc_persist_dir,
            )
        except FileNotFoundError as err:
            return SimpleDocumentStore()

    @cached_property
    def docstore(self):
        return PostgresDocumentStore.from_params(
            **self.pg_params
        )

    @cached_property
    def store(self):
        return self.docstore
