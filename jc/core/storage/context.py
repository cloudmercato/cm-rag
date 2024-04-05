from llama_index.core import StorageContext

from django.utils.functional import cached_property
from django.conf import settings

from core.storage.docstore import DocstoreManager
from core.storage.index import IndexStoreManager
from core.storage.graph_store import GraphStoreManager
from core.storage.vector_store import VectorStoreManager


class StorageManager:
    def __init__(
        self,
        embed_dim=settings.DEFAULT_EMBED_DIM,
        verbose=True
    ):
        self.embed_dim = embed_dim
        self.verbose = verbose

    @cached_property
    def docstore_manager(self):
        return DocstoreManager(
        )

    @cached_property
    def docstore(self):
        return self.docstore_manager.docstore

    @cached_property
    def index_store_manager(self):
        return IndexStoreManager(
        )

    @cached_property
    def index_store(self):
        return self.index_store_manager.index_store

    @cached_property
    def graph_store_manager(self):
        return GraphStoreManager(
        )

    @cached_property
    def graph_store(self):
        return self.graph_store_manager.graph_store

    @cached_property
    def vector_store_manager(self):
        return VectorStoreManager(
            embed_dim=self.embed_dim,
            verbose=self.verbose,
        )

    @cached_property
    def vector_store(self):
        return self.vector_store_manager.vector_store

    @cached_property
    def storage_context(self):
        storage_context = StorageContext.from_defaults(
            docstore=self.docstore,
            vector_store=self.vector_store,
            graph_store=self.graph_store,
            index_store=self.index_store,
        )
        return storage_context

    def flush(self):
        self.docstore_manager.flush()
        self.vector_store_manager.flush()
        self.index_store_manager.flush()
