import os

from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.graph_stores.falkordb import FalkorDBGraphStore

from django.conf import settings
from django.utils.functional import cached_property


class GraphStoreManager:
    @cached_property
    def graph_persist_dir(self):
        persist_path = os.path.join(settings.STORAGE_DIR, 'graph')
        return persist_path

    @cached_property
    def graph_persist_path(self):
        persist_path = os.path.join(self.graph_persist_dir, 'graph_store.json')
        return persist_path

    @cached_property
    def local_graph_store(self):
        return SimpleGraphStore.from_persist_dir(
            persist_dir=self.graph_persist_dir,
        )

    @cached_property
    def falkor_graph_store(self):
        return FalkorDBGraphStore(
            url=settings.FALKORDB_URL,
            decode_responses=True,
        )

    @cached_property
    def graph_store(self):
        if settings.FALKORDB_URL:
            return self.falkor_graph_store
        return self.local_graph_store

    def flush(self):
        self.graph_store._driver.flush()
        self.graph_store._driver.commit()
