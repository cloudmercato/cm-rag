from llama_index.core.tools import QueryEngineTool

from django.conf import settings
from django.utils.functional import cached_property

from core.indices import IndexManager
from core import models


class VectorIndexManager:
    def __init__(
        self,
        embed_dim=settings.DEFAULT_EMBED_DIM,
        verbose=True
    ):
        self.embed_dim = embed_dim
        self.verbose = verbose

    @cached_property
    def index_manager(self):
        return IndexManager()

    @cached_property
    def index(self):
        return self.index_manager.vectors.index

    @cached_property
    def query_engine(self):
        return self.index.as_query_engine()

    @cached_property
    def tools(self):
        vector_tool = QueryEngineTool.from_defaults(
            query_engine=self.query_engine,
            description=f"Useful for answering semantic questions about cloud providers",
        )
        return [vector_tool]

    def flush_index(self):
        self.index_manager.flush_index()

    def update_index(self, documents):
        return self.index_manager.update_index(documents)
