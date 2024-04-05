import os

from llama_index.vector_stores.postgres import PGVectorStore

from django.conf import settings
from django.utils.functional import cached_property

from core.storage.base import BaseSqlManager

TABLE_NAME = "cm_vectors"


class VectorStoreManager(BaseSqlManager):
    id_field = 'id'

    def __init__(
        self,
        embed_dim=settings.DEFAULT_EMBED_DIM,
        verbose=True
    ):
        self.embed_dim = embed_dim
        self.verbose = verbose

    @cached_property
    def vector_store(self):
        vector_store = PGVectorStore.from_params(
            table_name=TABLE_NAME,
            embed_dim=self.embed_dim,
            hybrid_search=True,  # TODO Correct or not
            text_search_config="english",
            **self.pg_params
        )
        return vector_store

    @cached_property
    def store(self):
        return self.vector_store

    @cached_property
    def table_name(self):
        return self.store.table_name
